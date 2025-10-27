from datetime import datetime, timedelta, timezone
import random
import secrets
from fastapi import HTTPException, status
from pydantic import EmailStr
from schemas.user_schema import UserCreate, UserReset
from models.user_model import User
from core.security import hash_password, verify_password
from typing import Optional, Union, Any
from uuid import UUID

class UserService:
    @staticmethod
    async def create_user(user_create: UserCreate) -> User:
        username = user_create.username.strip()
        email    = user_create.email.strip().lower()

        # TODO: checar por senhas fracas

        token = secrets.token_urlsafe(32)
        token_expiration = datetime.now(timezone.utc) + timedelta(hours=24)

        user = await User.find_one(User.email == email)

        if not user:
            user = User(
                username=username,
                email=email,
                hashed_password=hash_password(user_create.password),
                token_or_code=token,
                token_or_code_expiration=token_expiration
            )

            await user.save()
        elif not user.is_verified:
            await user.update({"$set": {"token_or_code": token, "token_or_code_expiration": token_expiration}})
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="O nome ou o e-mail já existe."
            )

        return user
    
    @staticmethod
    async def request_reset(email: EmailStr) -> Optional[str]:
        email = email.strip().lower()
        user = await User.find_one(User.email == email)

        reset_code = f"{random.randint(0, 999999):06}"
        hashed_code = hash_password(reset_code)
        expiration = datetime.now(timezone.utc) + timedelta(minutes=10)

        if user and user.is_verified:
            await user.update({"$set": {"token_or_code": hashed_code, "token_or_code_expiration": expiration}})
            return reset_code
        else:
            return None

    @staticmethod
    async def confirm_reset(email: EmailStr, code: str) -> bool:
        email = email.strip().lower()
        user = await UserService.authenticate_code(email, code)

        if not user or user.token_or_code_expiration < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido ou expirado")

        return True

    @staticmethod
    async def reset_password(data: UserReset) -> bool:
        email = data.email.strip().lower()
        user = await UserService.authenticate_code(email, data.token_or_code)

        if  not user or user.token_or_code_expiration >= datetime.now():
            await user.update({"$set": {"hashed_password": hash_password(data.password)}})

        return user

    @staticmethod
    async def verify_user(token: Union[str, Any]):
        user = await User.find_one(User.token_or_code == token)

        if not token or not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido ou expirado")

        await user.update({"$set": {"is_verified": True}})

        return {"msg": f"Seu e-mail foi verificado com sucesso! Você já pode fechar essa janela."}

    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == id)
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email)
        if not user or not user.is_verified:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        return user
    
    @staticmethod
    async def authenticate_code(email: str, code: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email)
        if not user or not user.is_verified:
            return None
        if not verify_password(code, user.token_or_code):
            return None

        return user

from fastapi import HTTPException, status
from schemas.user_schema import UserCreate
from models.user_model import User
from core.security import hash_password, verify_password
from typing import Optional, Union, Any
from uuid import UUID
import pymongo

class UserService:
    @staticmethod
    async def create_user(user_create: UserCreate) -> User:
        username = user_create.username.strip()
        email    = user_create.email.strip().lower()

        # TODO: checar por senhas fracas

        user_obj = User(
            username=username,
            email=email,
            hashed_password=hash_password(user_create.password)
        )

        try:
            await user_obj.save()
        except pymongo.errors.DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="O nome ou o e-mail já existe."
            )

        return user_obj
    
    @staticmethod
    async def verify_user(email: Union[str, Any]):
        if not email:
            raise HTTPException(status_code=400, detail="Token inválido ou expirado")

        user = await User.find_one(User.email == email)
        if not user:
            raise HTTPException(status_code=400, detail="Usuário não encontrado ou já verificado")
        await user.update({"$set": {"is_verified": True}})
        
        return {"msg": f"Email {email} verificado com sucesso!"}

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
        user = await UserService.get_user_by_email(email=email)
        if not user or not user.is_verified:
            return None
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None            

        return user

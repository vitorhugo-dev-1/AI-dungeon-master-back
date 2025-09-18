from passlib.context import CryptContext
from typing import Union, Any, Optional
from datetime import datetime, timedelta, timezone
from jose import jwt
from core.config import settings

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

def create_token(
    subject: Union[str, Any],
    secret_key: str = settings.JWT_SECRET_KEY,
    expires_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    expires_delta = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    info_jwt = {
        "exp": expires_delta,
        "sub": str(subject)
    }

    return jwt.encode(
        info_jwt,
        secret_key,
        settings.ALGORITHM
    )

def create_access_token(subject: Union[str, Any], expires_minutes: Optional[int] = None) -> str:
    return create_token(subject, expires_minutes=expires_minutes)

def create_refresh_token(subject: Union[str, Any], expires_minutes: Optional[int] = None) -> str:
    return create_token(subject, settings.JWT_REFRESH_SECRET_KEY, expires_minutes=expires_minutes)

def create_verification_token(subject: Union[str, Any]):
    return create_token(subject, expires_minutes=60*24)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload["sub"]
    except Exception:
        return None
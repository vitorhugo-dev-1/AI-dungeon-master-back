from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description='E-mail Usuário')
    username: str = Field(..., description='Username Usuário')
    password: str = Field(..., min_length=5, max_length=255, description='Senha Usuário')

class UserDetail(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    is_verified: Optional[bool]
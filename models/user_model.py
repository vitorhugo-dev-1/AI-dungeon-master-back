from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import Field, EmailStr
from typing import Annotated, Optional
from datetime import datetime

class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: Annotated[str, Indexed(str, unique=True)]
    email: Annotated[str, Indexed(EmailStr, unique=True)]
    hashed_password: str
    disabled: Optional[bool] = None

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return f"<User {self.email}>"

    def __hash__(self) -> int:
        return hash(self.email)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False
    
    @property
    def create(self) -> datetime:
        return self.id.generation_time
    
    @classmethod
    async def by_email(self, email: str) -> "User":
        return await self.find_one(self.email == email)
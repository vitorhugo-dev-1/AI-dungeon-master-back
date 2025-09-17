from beanie import Document, Indexed, Link, before_event, Replace, Insert
from uuid import UUID, uuid4
from pydantic import Field, model_validator
from typing import Annotated, Optional
from datetime import datetime, timezone
from .user_model import User

class Personagem(Document):
    personagem_id: UUID = Field(default_factory=uuid4, unique=True)
    nome: Annotated[str, Indexed(str)]
    classe: str
    raca: str
    pv_max: int
    pv_num: int | None = None
    pe_max: int
    pe_num: int | None = None
    gold: int
    disabled: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    owner: Link[User]

    def __repr__(self) -> str:
        return f"<Personagem f{self.nome}>"
    
    def __str__(self) -> str:
        return self.nome
    
    def __hash__(self) -> int:
        return hash(self.nome)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Personagem):
            return self.personagem_id == other.personagem_id
        return False

    @model_validator(mode="after")
    def set_starting_values(self):
        if self.pv_num is None or self.pv_num > self.pv_max:
            self.pv_num = self.pv_max
        if self.pe_num is None or self.pe_num > self.pe_max:
            self.pe_num = self.pe_max
        return self

    @before_event([Replace, Insert])
    def sync_update_at(self):
        self.updated_at = datetime.now(timezone.utc)

from beanie import Document, Indexed, before_event, Replace, Insert
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Annotated, Any, Dict, Optional, Union
from datetime import datetime, timezone
from schemas.personagem_schema import PersonagemUpdate

class Resposta(BaseModel):
    narracao: str
    sugestoes: list[str]
    mod_status: Optional[PersonagemUpdate] = None
    combat: Optional[Dict[str, Any]] = None

class Prompt(BaseModel):
    acao: str
    rolagem: Optional[int] = None
    atr: Optional[str] = None

class Campanha(Document):
    campanha_id: UUID = Field(default_factory=uuid4, unique=True)
    titulo: Annotated[str, Indexed(str)]
    descricao: str
    personagem: UUID
    events: list[Union[Resposta, Prompt]] = Field(default_factory=list)
    disabled: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    owner: UUID

    def __repr__(self) -> str:
        return f"<Campanha {self.titulo}>"

    def __str__(self) -> str:
        return self.titulo

    def __hash__(self) -> int:
        return hash(self.titulo)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Campanha):
            return self.campanha_id == other.campanha_id
        return False

    @before_event([Replace, Insert])
    def sync_update_at(self):
        self.updated_at = datetime.now(timezone.utc)

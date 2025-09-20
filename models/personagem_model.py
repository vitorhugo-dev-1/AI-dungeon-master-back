from beanie import Document, Indexed, Link, before_event, Replace, Insert
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime, timezone
from models.user_model import User

class Atributos(BaseModel):
    STR: int
    AGI: int
    RES: int
    INT: int
    PER: int
    DET: int

class Stats(BaseModel):
    pv_max: int
    pe_max: int
    pv: int
    pe: int
    gold: int

    @classmethod
    def from_atributos(cls, atr: Atributos) -> "Stats":
        calc_pv_max = 10 + atr.RES * 4 + atr.STR
        calc_pe_max = 5 + atr.RES * 2 + atr.AGI
        return cls(
            pv_max=calc_pv_max,
            pe_max=calc_pe_max,
            pv=calc_pv_max,
            pe=calc_pe_max,
            gold=50
        )

class Personagem(Document):
    personagem_id: UUID = Field(default_factory=uuid4, unique=True)
    nome: Annotated[str, Indexed(str)]
    classe: str
    raca: str
    origens: str
    level: int = 1
    xp: int = 0
    atr: Atributos
    stats: Stats
    itens: list[str]
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

    @before_event([Replace, Insert])
    def sync_update_at(self):
        self.updated_at = datetime.now(timezone.utc)

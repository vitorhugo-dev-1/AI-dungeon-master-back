from beanie import Link
from pydantic import BaseModel, Field
from typing import Optional, Union
from uuid import UUID
from datetime import datetime
from models.personagem_model import Personagem
from schemas.personagem_schema import PersonagemUpdate

class Inimigo(BaseModel):
    inimigo_id: str
    nome: str
    pv: int
    pe: int
    gold: int
    itens: Optional[list[str]] = None
    status: str

class Combat(BaseModel):
    ordem: list[str]
    turno: int
    inimigos: list[Inimigo]

class Resposta(BaseModel):
    narracao: str = Field(..., description='Narração LLM')
    sugestoes: list[str]
    mod_status: Optional[PersonagemUpdate] = None
    combat: Optional[Combat] = None

class Prompt(BaseModel):
    acao: str
    rolagem: Optional[int] = None
    atr: Optional[str] = None

class CampanhaCreate(BaseModel):
    titulo: str = Field(..., max_length=50, description='Titulo campanha')
    descricao: str = Field(..., max_length=255, description='Descrição campanha')
    personagem_id: UUID
    events: Optional[list[Union[Resposta, Prompt]]] = Field(default_factory=list)

class CampanhaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    events: Optional[list[Union[Resposta, Prompt]]] = None
    disabled: Optional[bool] = None

class CampanhaDetail(BaseModel):
    campanha_id: UUID
    titulo: str
    descricao: str
    personagem: UUID
    events: list[Union[Resposta, Prompt]]
    disabled: bool = False
    owner: UUID
    created_at: datetime
    updated_at: datetime

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class PersonagemCreate(BaseModel):
    nome:   str = Field(..., max_length=50, description='Nome Personagem')
    classe: str = Field(..., max_length=20, description='Classe Personagem')
    raca:   str = Field(..., max_length=20, description='Raça Personagem')
    pv_max: int = Field(..., ge=1, description='Pontos de Vida Máximos Personagem')
    pe_max: int = Field(..., ge=1, description='Pontos de Energia Máximos Personagem')
    gold:   int = Field(..., ge=0, description='Moedas de ouro Personagem')

class PersonagemUpdate(BaseModel):
    nome:   Optional[str] = None
    classe: Optional[str] = None
    raca:   Optional[str] = None
    pv_max: Optional[int] = None
    pe_max: Optional[int] = None
    gold:   Optional[int] = None

class PersonagemDetail(BaseModel):
    personagem_id: UUID
    nome:   str
    classe: str
    raca:   str
    pv_max: int
    pv_num: int
    pe_max: int
    pe_num: int
    gold:   int
    disabled: bool
    created_at: datetime
    updated_at: datetime
    
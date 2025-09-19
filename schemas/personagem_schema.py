from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from models.personagem_model import Stats

class Atributos(BaseModel):
    STR: int = Field(..., ge=1, le=5, description="Força")
    AGI: int = Field(..., ge=1, le=5, description="Agilidade")
    RES: int = Field(..., ge=1, le=5, description="Resistência")
    INT: int = Field(..., ge=1, le=5, description="Inteligência")
    PER: int = Field(..., ge=1, le=5, description="Percepção")
    DET: int = Field(..., ge=1, le=5, description="Determinação")

class AtributosUpdate(BaseModel):
    STR: Optional[int] = Field(None, ge=1, le=5, description="Força")
    AGI: Optional[int] = Field(None, ge=1, le=5, description="Agilidade")
    RES: Optional[int] = Field(None, ge=1, le=5, description="Resistência")
    INT: Optional[int] = Field(None, ge=1, le=5, description="Inteligência")
    PER: Optional[int] = Field(None, ge=1, le=5, description="Percepção")
    DET: Optional[int] = Field(None, ge=1, le=5, description="Determinação")

class PersonagemCreate(BaseModel):
    nome:    str = Field(..., max_length=50, description='Nome Personagem')
    classe:  str = Field(..., max_length=20, description='Classe Personagem')
    raca:    str = Field(..., max_length=20, description='Raça Personagem')
    origens: str = Field(..., max_length=50, description='Origens Personagem')
    atr:     Atributos

class PersonagemUpdate(BaseModel):
    nome:    Optional[str] = None
    classe:  Optional[str] = None
    raca:    Optional[str] = None
    origens: Optional[str] = None
    atr:     Optional[AtributosUpdate] = None
    stats:   Optional[Stats] = None

class PersonagemDetail(BaseModel):
    personagem_id: UUID
    nome:   str
    classe: str
    raca:   str
    level:  int
    xp:     int
    atr:    Atributos
    stats:  Stats
    disabled: bool
    created_at: datetime
    updated_at: datetime

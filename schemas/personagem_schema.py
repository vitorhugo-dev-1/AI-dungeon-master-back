from pydantic import BaseModel, Field

class PersonagemAuth(BaseModel):
    nome:   str = Field(..., max_length=50, description='Nome Personagem')
    classe: str = Field(..., max_length=20, description='Classe Personagem')
    raca:   str = Field(..., max_length=20, description='Raça Personagem')
    pv_max: int = Field(..., ge=1, description='Pontos de Vida Máximos Personagem')
    pv_num: int = Field(..., ge=0, description='Pontos de Vida Atuais Personagem')
    pe_max: int = Field(..., ge=1, description='Pontos de Energia Máximos Personagem')
    pe_num: int = Field(..., ge=0, description='Pontos de Energia Atuais Personagem')
    gold:   int = Field(..., ge=0, description='Moedas de ouro Personagem')

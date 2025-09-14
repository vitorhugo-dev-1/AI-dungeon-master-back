from pydantic import BaseModel

class Personagem(BaseModel):
    nome: str
    classe: str
    raca: str
    pv_max: int
    pv_num: int
    pe_max: int
    pe_num: int
    gold: int

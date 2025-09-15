from beanie import Document
from datetime import datetime

class Personagem(Document):
    nome: str
    classe: str
    raca: str
    pv_max: int
    pv_num: int
    pe_max: int
    pe_num: int
    gold: int

    @property
    def create(self) -> datetime:
        return self.id.generation_time

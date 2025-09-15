from schemas.personagem_schema import PersonagemAuth
from models.personagem_model import Personagem

class PersonagemService:
    @staticmethod
    async def create_personagem(personagem: PersonagemAuth):
        personagem = Personagem(
            nome = personagem.nome,
            classe = personagem.classe,
            raca = personagem.raca,
            pv_max = personagem.pv_max,
            pv_num = personagem.pv_num,
            pe_max = personagem.pe_max,
            pe_num = personagem.pe_num,
            gold = personagem.gold
        )
        await personagem.save()
        return personagem
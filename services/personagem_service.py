from models.user_model import User
from models.personagem_model import Personagem
from typing import List
from schemas.personagem_schema import PersonagemCreate, PersonagemUpdate
from uuid import UUID

class PersonagemService:
    @staticmethod
    async def list_personagem(user: User) -> List[Personagem]:
        personagens = await Personagem.find(Personagem.owner.id == user.id).to_list()
        return personagens

    @staticmethod
    async def create_personagem(user: User, data: PersonagemCreate) -> Personagem:
        personagem = Personagem(**data.model_dump(), owner=user)
        return await personagem.insert()

    @staticmethod
    async def detail_personagem(user: User, personagem_id: UUID):
        personagem = await Personagem.find_one(
            Personagem.personagem_id == personagem_id,
            Personagem.owner.id == user.id
        )
        return personagem

    @staticmethod
    async def update_personagem(user: User, personagem_id: UUID, data: PersonagemUpdate):
        personagem = await PersonagemService.detail_personagem(user, personagem_id)
        await personagem.set(data.model_dump(exclude_unset=True))
        return personagem

    @staticmethod
    async def delete_personagem(user: User, personagem_id: UUID):
        personagem = await PersonagemService.detail_personagem(user, personagem_id)
        if not personagem:
            return None
        deleted_personagem = personagem
        await personagem.delete()
        return deleted_personagem

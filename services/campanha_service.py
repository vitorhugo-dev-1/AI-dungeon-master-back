from fastapi import HTTPException, status
from models.personagem_model import Personagem
from models.user_model import User
from models.campanha_model import Campanha
from typing import List
from schemas.campanha_schema import CampanhaCreate, CampanhaUpdate
from uuid import UUID

class CampanhaService:
    @staticmethod
    async def list_campanha(user: User) -> List[Campanha]:
        campanhas = await Campanha.find(Campanha.owner == user.user_id).to_list()
        return campanhas

    @staticmethod
    async def create_campanha(user: User, data: CampanhaCreate) -> Campanha:
        personagem = await Personagem.find_one(Personagem.personagem_id == data.personagem_id)
        campanha = Campanha(
            **data.model_dump(),
            personagem = personagem.personagem_id,
            owner=user.user_id,
        )
        return await campanha.insert()

    @staticmethod
    async def detail_campanha(user: User, campanha_id: UUID):
        campanha = await Campanha.find_one(
            Campanha.campanha_id == campanha_id,
            Campanha.owner == user.user_id
        )
        return campanha

    @staticmethod
    async def update_campanha(user: User, campanha_id: UUID, data: CampanhaUpdate):
        campanha = await CampanhaService.detail_campanha(user, campanha_id)
        await campanha.set(data.model_dump(exclude_unset=True))
        return campanha

    @staticmethod
    async def delete_campanha(user: User, campanha_id: UUID):
        campanha = await CampanhaService.detail_campanha(user, campanha_id)
        if not campanha:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campanha não encontrada."
            )
        deleted_campanha = campanha
        await campanha.delete()
        return deleted_campanha

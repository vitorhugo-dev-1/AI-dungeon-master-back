from typing import List
from fastapi import APIRouter, Depends
from models.user_model import User
from schemas.personagem_schema import PersonagemCreate, PersonagemUpdate, PersonagemDetail
from services.personagem_service import PersonagemService
from api.dependencies.user_deps import get_current_user
from uuid import UUID

personagem_router = APIRouter()

@personagem_router.get("/", summary="Lista todos os personagens", response_model=List[PersonagemDetail])
async def list_personagem(current_user: User = Depends(get_current_user)):
    return await PersonagemService.list_personagem(current_user)

@personagem_router.post("/", summary="Cadastra um novo personagem", response_model=PersonagemDetail)
async def create_personagem(data: PersonagemCreate, current_user: User = Depends(get_current_user)):
    return await PersonagemService.create_personagem(current_user, data)

@personagem_router.get("/{personagem_id}", summary="Detalha personagem com ID específico", response_model=PersonagemDetail)
async def detail_personagem(personagem_id: UUID, current_user: User = Depends(get_current_user)):
    return await PersonagemService.detail_personagem(current_user, personagem_id)

@personagem_router.put("/{personagem_id}", summary="Atualiza personagem com ID específico", response_model=PersonagemDetail)
async def update_personagem(personagem_id: UUID, data: PersonagemUpdate, current_user: User = Depends(get_current_user)):
    return await PersonagemService.update_personagem(current_user, personagem_id, data)

@personagem_router.delete("/{personagem_id}", summary="Exclui personagem com ID específico", response_model=PersonagemDetail)
async def delete_personagem(personagem_id: UUID, current_user: User = Depends(get_current_user)):
    return await PersonagemService.delete_personagem(current_user, personagem_id)

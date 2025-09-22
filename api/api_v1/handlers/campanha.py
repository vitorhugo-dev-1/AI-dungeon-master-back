from typing import List
from fastapi import APIRouter, Depends
from models.user_model import User
from schemas.campanha_schema import CampanhaCreate, CampanhaUpdate, CampanhaDetail
from services.campanha_service import CampanhaService
from api.dependencies.user_deps import get_current_user
from uuid import UUID

campanha_router = APIRouter()

@campanha_router.get("/", summary="Lista todas as campanhas", response_model=List[CampanhaDetail])
async def list_campanha(current_user: User = Depends(get_current_user)):
    return await CampanhaService.list_campanha(current_user)

@campanha_router.post("/", summary="Cadastra uma nova campanha", response_model=CampanhaDetail)
async def create_campanha(data: CampanhaCreate, current_user: User = Depends(get_current_user)):
    return await CampanhaService.create_campanha(current_user, data)

@campanha_router.get("/{campanha_id}", summary="Detalha campanha com ID específico", response_model=CampanhaDetail)
async def detail_campanha(campanha_id: UUID, current_user: User = Depends(get_current_user)):
    return await CampanhaService.detail_campanha(current_user, campanha_id)

@campanha_router.put("/{campanha_id}", summary="Atualiza campanha com ID específico", response_model=CampanhaDetail)
async def update_campanha(campanha_id: UUID, data: CampanhaUpdate, current_user: User = Depends(get_current_user)):
    return await CampanhaService.update_campanha(current_user, campanha_id, data)

@campanha_router.delete("/{campanha_id}", summary="Exclui campanha com ID específico", response_model=CampanhaDetail)
async def delete_campanha(campanha_id: UUID, current_user: User = Depends(get_current_user)):
    return await CampanhaService.delete_campanha(current_user, campanha_id)

from fastapi import APIRouter, Depends
from models.user_model import User
from services.historico_service import HistoricoService
from api.dependencies.user_deps import get_current_user
from uuid import UUID

historico_router = APIRouter()

@historico_router.get("/{campanha_id}", summary="Lista todas as mensagens de uma campanha com ID específico")
async def list_historico(campanha_id: UUID, current_user: User = Depends(get_current_user)):
    return await HistoricoService.list_historico(current_user, campanha_id)

from fastapi import APIRouter
from api.api_v1.handlers import user
from api.api_v1.handlers import personagem
from api.api_v1.handlers import campanha
from api.api_v1.handlers import historico
from api.api_v1.handlers import websocket
from api.auth.jwt import auth_router

router = APIRouter()

router.include_router(
    user.user_router,
    prefix='/users',
    tags=['users']
)
router.include_router(
    auth_router,
    prefix='/auth',
    tags=['auth']
)
router.include_router(
    personagem.personagem_router,
    prefix='/personagem',
    tags=['personagem']
)
router.include_router(
    campanha.campanha_router,
    prefix='/campanha',
    tags=['campanha']
)
router.include_router(
    historico.historico_router,
    prefix='/historico',
    tags=['historico']
)
router.include_router(
    websocket.websocket_router,
    prefix='/ws',
    tags=['ws']
)
from fastapi import APIRouter
from api.api_v1.handlers import user
from api.api_v1.handlers import personagem
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
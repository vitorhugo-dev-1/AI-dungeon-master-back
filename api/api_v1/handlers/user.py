from fastapi import APIRouter, BackgroundTasks, Depends
from schemas.user_schema import UserCreate, UserDetail
from services.user_service import UserService
from models.user_model import User
from api.dependencies.user_deps import get_current_user
from core.email import send_verification_email
from core.security import create_verification_token, verify_token

user_router = APIRouter()

@user_router.post('/adiciona', summary='Adiciona Usuário', response_model=UserDetail)
async def adiciona_usuario(data: UserCreate, background_tasks: BackgroundTasks):
    user =  await UserService.create_user(data)
    token = create_verification_token(user.email)
    background_tasks.add_task(send_verification_email, user.email, token)
    return user

@user_router.get('/me', summary='Detalhes do Usuário Logado', response_model=UserDetail)
async def get_me(user: User = Depends(get_current_user)):
    return user

@user_router.get("/verifica")
async def verify(token: str):
    email = verify_token(token)
    return await UserService.verify_user(email)

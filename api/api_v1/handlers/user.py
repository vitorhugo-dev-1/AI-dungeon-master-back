from fastapi import APIRouter, BackgroundTasks, Depends
from schemas.user_schema import UserConfirmReset, UserCreate, UserDetail, UserRequestReset, UserReset
from services.user_service import UserService
from models.user_model import User
from api.dependencies.user_deps import get_current_user
from core.email import send_reset_email, send_verification_email
from core.security import create_verification_token, verify_token

user_router = APIRouter()

@user_router.post('/adiciona', summary='Adiciona Usuário', response_model=UserDetail)
async def adiciona_usuario(data: UserCreate, background_tasks: BackgroundTasks):
    user = await UserService.create_user(data)
    token = create_verification_token(user.token_or_code)
    background_tasks.add_task(send_verification_email, user.email, token)
    return user

@user_router.post('/request-reset', summary='Inicia redefinição de senha')
async def inicia_reset(data: UserRequestReset, background_tasks: BackgroundTasks):
    code = await UserService.request_reset(data.email)

    if code:
        background_tasks.add_task(send_reset_email, data.email, code)

    return {"detail": "Se existir uma conta com este e-mail, enviaremos um código para redefinir a senha."}

@user_router.post('/confirma-reset', summary='Confirma redefinição de senha')
async def confirma_reset(data: UserConfirmReset):
    response = await UserService.confirm_reset(data.email, data.token_or_code)
    return {"detail": response}

@user_router.post('/reset-senha', summary='Redefine a senha')
async def reset_senha(data: UserReset):
    user = await UserService.reset_password(data)
    return user

@user_router.get('/me', summary='Detalhes do Usuário Logado', response_model=UserDetail)
async def get_me(user: User = Depends(get_current_user)):
    return user

@user_router.get("/verifica")
async def verify(token: str):
    decoded_token = verify_token(token)
    return await UserService.verify_user(decoded_token)

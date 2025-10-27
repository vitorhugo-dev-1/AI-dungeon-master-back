from fastapi_mail import FastMail, MessageSchema
from core.config import settings

async def send_verification_email(email: str, token: str):
    verification_url = f"http://localhost:8000{settings.API_V1_STR}/users/verifica?token={token}"

    message = MessageSchema(
        subject="Verifique sua conta",
        recipients=[email],
        body=f"Clique no link para verificar: {verification_url}",
        subtype="plain"
    )
    fm = FastMail(settings.EMAIL)
    await fm.send_message(message)

async def send_reset_email(email: str, code: str):
    message = MessageSchema(
        subject="Redefinição de senha",
        recipients=[email],
        body=f"Use este código para redefinir sua senha: {code}",
        subtype="plain"
    )
    fm = FastMail(settings.EMAIL)
    await fm.send_message(message)

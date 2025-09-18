from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
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

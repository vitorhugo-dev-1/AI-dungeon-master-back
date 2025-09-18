from typing import List
from decouple import config
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from fastapi_mail import ConnectionConfig

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:4200"
    ]
    PROJECT_NAME: str = "DungeonMind"
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)

    # Email settings
    EMAIL: object = ConnectionConfig(
        MAIL_USERNAME = config("MAIL_USERNAME", cast=str),
        MAIL_PASSWORD = config("MAIL_PASSWORD", cast=str),  # app password
        MAIL_FROM = config("MAIL_FROM", cast=str),
        MAIL_PORT = 465,
        MAIL_SERVER = config("MAIL_SERVER", cast=str),
        MAIL_FROM_NAME = config("MAIL_FROM_NAME", cast=str),
        MAIL_STARTTLS = False,
        MAIL_SSL_TLS = True,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )

    class Config:
        case_sensitive = True

settings = Settings()
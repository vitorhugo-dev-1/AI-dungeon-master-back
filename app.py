from contextlib import asynccontextmanager

from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.api_v1.router import router

from models.user_model import User
from models.personagem_model import Personagem

async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db = client.dungeon_mind

    await init_beanie(
        database=db,
        document_models=[
            User,
            Personagem
        ],
    )

    yield

    client.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    router, 
    prefix=settings.API_V1_STR
)
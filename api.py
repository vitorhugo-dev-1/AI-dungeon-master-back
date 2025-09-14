from fastapi import FastAPI
from routes.personagem import personagem_router
from fastapi.middleware.cors import CORSMiddleware

cliente_app = {
    "http://localhost:4200/"
}

app = FastAPI()
ApiPrefix = "/api/v1"

app.include_router(personagem_router, prefix=ApiPrefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins = cliente_app,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
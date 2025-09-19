from fastapi import APIRouter
from fastapi.responses import RedirectResponse

root_router = APIRouter()

@root_router.get("/", summary='Status da API')
def read_root():
    return {"status": "ok", "message": "API is running"}

@root_router.get("/favicon.ico")
def favicon():
    return RedirectResponse("/static/favicon.ico")

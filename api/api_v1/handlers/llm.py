from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from api.dependencies.user_deps import get_current_user
from models.user_model import User
from services.llm_service import stream_response

llm_router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@llm_router.post("/chat/")
async def chat(request: PromptRequest, current_user: User = Depends(get_current_user)):
    return StreamingResponse(stream_response(request.prompt), media_type="text/plain")
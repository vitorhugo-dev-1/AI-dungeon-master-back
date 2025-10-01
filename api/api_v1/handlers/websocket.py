from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from services.websocket_service import WebSocketLLMService
from api.dependencies.user_deps import get_current_user

websocket_router = APIRouter()

@websocket_router.websocket("")
async def websocket_llm(websocket: WebSocket):
    await websocket.accept()
    user = None

    try:
        while True:
            try:
                data = await websocket.receive_json()
            except WebSocketDisconnect:
                print(f"Cliente {user.user_id if user else 'desconhecido'} desconectou")
                break
            except Exception as e:
                print("Erro ao receber JSON:", e)
                if not websocket.client_state.name == "DISCONNECTED":
                    await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
                break

            token = data.get("token")
            prompt = data.get("prompt")
            campanha = data.get("campanha_id")

            if user is None:
                user = await get_current_user(token)
                if not user:
                    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                    break

            if not prompt:
                await websocket.send_json({"error": "Prompt ausente"})
                continue

            try:
                if not campanha:
                    async for partial in WebSocketLLMService.generate_campanha(user, personagem_id=UUID(prompt)):
                        data = {
                            "campanha_id": partial['campanha_id'],
                            "text": partial['text']
                        }
                        await websocket.send_json(data)
            except WebSocketDisconnect:
                print(f"Cliente {user.user_id} desconectou durante o streaming")
                break
            except Exception as e:
                print(f"Erro no streaming para {user.user_id}:", e)
                await websocket.send_json({"error": "Erro interno no servidor"})

    finally:
        print(f"Conexão encerrada para {user.user_id if user else 'desconhecido'}")

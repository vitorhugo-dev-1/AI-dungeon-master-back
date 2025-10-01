import asyncio
from uuid import UUID
from groq import Groq
from core.config import settings
from models.personagem_model import Personagem
from models.user_model import User
from schemas.campanha_schema import CampanhaCreate, CampanhaUpdate, Resposta
from services.campanha_service import CampanhaService
from json_repair import repair_json
import json

client = Groq(api_key=settings.GROQ_API_KEY)

def parse_json_safe(string: str, default=None):
    try:
        return json.loads(string)
    except (json.JSONDecodeError, TypeError):
        return default

class WebSocketLLMService:
    @staticmethod
    async def stream_response(prompt: str):
        full_text = ""

        def sync_stream():
            return client.chat.completions.create(
                model='qwen/qwen3-32b',
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_completion_tokens=4096,
                top_p=0.95,
                reasoning_effort='none',
                stream=True,
            )

        completion = await asyncio.to_thread(sync_stream)

        for chunk in completion:
            text = chunk.choices[0].delta.content
            if text is not None:
                full_text += text
                yield full_text
            await asyncio.sleep(0.01)

    @staticmethod
    async def generate_campanha(user: User, personagem_id: UUID):
        full_text = ""

        personagem = await Personagem.find_one(Personagem.personagem_id == personagem_id)

        prompt = f"""Mestre uma aventura de RPG para mim. Mantenha as repostas concisas e engajantes.

            O personagem com quem vou jogar será {personagem.nome}, um {personagem.classe} {personagem.raca}
            com os seguintes backgrounds: {personagem.origens[0]} e {personagem.origens[1]}.

            Sua resposta deve ser em formato JSON com o seguinte padrão:
            {{
                "titulo": "Titulo com menos de 51 caracteres",
                "descricao": "Breve sinopse com menos de 256 caracteres",
                "narracao": "Sua descrição inicial da aventura",
                "sugestoes": ["Inclua de 2 a 4 sugestões sobre o que o jogador pode fazer em seguida"]
            }}
            NOTA: os campos "titulo" e "descricao" só devem aparecer na sua primeira resposta
            
            Sinta-se livre para estilizar "narracao" e "sugestoes" com markdown"""

        def sync_stream():
            return client.chat.completions.create(
                model='qwen/qwen3-32b',
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=4096,
                top_p=0.95,
                reasoning_effort='none',
                stream=True,
            )

        create_data = CampanhaCreate(titulo="", descricao='', personagem_id=personagem.personagem_id)
        campanha = await CampanhaService.create_campanha(user, create_data)

        completion = await asyncio.to_thread(sync_stream)

        for chunk in completion:
            text = chunk.choices[0].delta.content
            if text is not None:
                full_text += text
                response = repair_json(full_text, ensure_ascii=False)
                parsed = parse_json_safe(response)

                if hasattr(parsed, "narracao") and not campanha.titulo and not campanha.descricao:
                    data = CampanhaUpdate(titulo=parsed['titulo'], descricao=parsed['descricao'])
                    await CampanhaService.update_campanha(user, campanha.campanha_id, data)

                yield { "campanha_id": str(campanha.campanha_id), "text": response }
            else:
                parsed = repair_json(full_text, return_objects=True, ensure_ascii=False)
                events = Resposta(narracao=parsed['narracao'], sugestoes=parsed['sugestoes'])
                data = CampanhaUpdate(
                    titulo=parsed['titulo'],
                    descricao=parsed['descricao'],
                    events=campanha.events + [events]
                )

                await CampanhaService.update_campanha(user, campanha.campanha_id, data)
            await asyncio.sleep(0.01)

from pydantic import BaseModel
from models.user_model import User
from models.campanha_model import Campanha
from uuid import UUID

class HistoricoDetail(BaseModel):
    events: list

class HistoricoService:
    @staticmethod
    async def list_historico(user: User, campanha_id: UUID):
        historico = await Campanha.find_one(
            Campanha.campanha_id == campanha_id,
            Campanha.owner == user.user_id,
            projection_model=HistoricoDetail
        )
        campos_a_manter = {"acao", "narracao"}
        events_sem_nulls = [
            {key: value for key, value in event.items() if value is not None}
            for event in historico.events
        ]
        events_com_filtro = [
            {key: value for key, value in event.items() if key in campos_a_manter}
            for event in events_sem_nulls
        ]

        historico_llm = []
        for item in events_com_filtro:
            if "narracao" in item:
                historico_llm.append({"role": "assistant", "content": item["narracao"]})
            elif "acao" in item:
                historico_llm.append({"role": "user", "content": item["acao"]})

        return historico_llm

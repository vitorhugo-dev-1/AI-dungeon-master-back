from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId
from models.personagem_model import Personagem
from schemas.personagem_schema import PersonagemAuth

personagem_router = APIRouter()

@personagem_router.get("/", summary="Lista todos os personagens")
async def lista_personagens():
    personagens = await Personagem.find_all().to_list()
    return personagens

@personagem_router.get("/{personagem_id}", summary="Busca por personagem com ID específico")
async def busca_personagem_id(personagem_id: PydanticObjectId):
    personagem = await Personagem.get(personagem_id)
    if not personagem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personagem não encontrado"
        )
    return personagem

@personagem_router.post("/", summary="Cadastra um novo personagem")
async def cadastra_personagens(personagem: PersonagemAuth):
    novo_personagem = Personagem(**personagem.model_dump())
    await novo_personagem.insert()
    return novo_personagem

@personagem_router.put("/{personagem_id}", summary="Atualiza personagem com ID específico")
async def atualiza_personagem(personagem_id: PydanticObjectId, personagem: PersonagemAuth):
    personagem_existente = await Personagem.get(personagem_id)
    if not personagem_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personagem não encontrado"
        )

    await personagem_existente.set(personagem.dict())
    return personagem_existente

@personagem_router.delete("/{personagem_id}", summary="Exclui personagem com ID específico")
async def exclui_personagem(personagem_id: PydanticObjectId):
    personagem = await Personagem.get(personagem_id)
    if not personagem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personagem não encontrado"
        )

    await personagem.delete()
    return personagem

from fastapi import APIRouter
from config.database import conexao
from models.personagem import Personagem
from schemas.personagem import personagemEntidade, listaPersonagensEntidade
from bson import ObjectId

personagem_router = APIRouter()

@personagem_router.get("/personagem")
async def lista_personagens():
    return listaPersonagensEntidade(conexao.local.personagem.find())

@personagem_router.get("/personagem/{personagem_id}")
async def busca_personagem_id(personagem_id):
    return personagemEntidade(
        conexao.local.personagem.find_one(
            { "_id": ObjectId(personagem_id) }
        )
    )

@personagem_router.post("/personagem")
async def cadastra_personagens(personagem: Personagem):
    result = conexao.local.personagem.insert_one(dict(personagem))
    return personagemEntidade(
        conexao.local.personagem.find_one(
            { "_id": ObjectId(result.inserted_id) }
        )
    )

@personagem_router.put("/personagem/{personagem_id}")
async def atualiza_personagem(personagem_id, personagem: Personagem):
    conexao.local.personagem.find_one_and_update(
        { "_id": ObjectId(personagem_id) },
        { "$set": dict(personagem) }
    )

    return personagemEntidade(
        conexao.local.personagem.find_one(
            { "_id": ObjectId(personagem_id) } 
        )
    )

@personagem_router.delete("/personagem/{personagem_id}")
async def exclui_personagem(personagem_id):
    return personagemEntidade(
        conexao.local.personagem.find_one_and_delete(
            { "_id": ObjectId(personagem_id) }
        )
    )

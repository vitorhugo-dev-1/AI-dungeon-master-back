## DungeonMind — Backend (AI Dungeon Master)

Backend em Python/FastAPI para um sistema de "Dungeon Master" que usa IA.

Este repositório contém a API backend construída com FastAPI, Beanie (ODM para MongoDB), autenticação JWT, envio de e-mails e suporte a WebSockets para comunicação em tempo real.

### Principais tecnologias

- Python + FastAPI
- Beanie + Motor (MongoDB)
- JWT (python-jose)
- FastAPI-Mail (envio de e-mail via SMTP)
- WebSockets
- Uvicorn (ASGI server)

## Estrutura principal

- `app.py` — ponto de entrada da aplicação (instancia FastAPI, inicializa Beanie/MongoDB e registra rotas).
- `api/` — rotas e handlers da API (v1).
- `core/config.py` — configurações da aplicação (usa `decouple`/`.env`).
- `models/` — modelos Beanie para MongoDB.
- `schemas/` — Pydantic schemas.
- `services/` — lógica de negócio e integrações (e-mail, websockets, etc.).
- `auth/`, `dependencies/` — autenticação e dependências compartilhadas.
- `requirements.txt` — dependências do projeto.

## Pré-requisitos

- Python 3.11+
- MongoDB rodando e acessível pela variável `MONGO_CONNECTION_STRING`
- Uma conta de e-mail com suporte a SMTP (ex.: Gmail com app password) para envio de mensagens
- Uma chave de API do Groq

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com os valores apropriados. Não comite suas chaves reais.

Exemplo (`.env.example`):

```properties
JWT_SECRET_KEY=sua_chave_secreta
JWT_REFRESH_SECRET_KEY=sua_outra_chave_secreta
MONGO_CONNECTION_STRING=mongodb://localhost:27017
MAIL_USERNAME=exemplo
MAIL_PASSWORD=sua_senha_de_aplicacao
MAIL_FROM=exemplo@email.com
MAIL_SERVER=seu servidor SMTP de email
MAIL_FROM_NAME=Nome de exibição do e-mail
GROQ_API_KEY=sua_chave_da_api_do_groq
```

Observações sobre as variáveis:
- `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY`: chaves usadas para assinar tokens JWT.
- `MONGO_CONNECTION_STRING`: string de conexão para o MongoDB.
- `MAIL_*`: configurações para envio de e-mail (o projeto usa `fastapi-mail`).
- `GROQ_API_KEY`: chave para integração com serviços que usam GROQ.

Algumas configurações possuem valores padrão em `core/config.py`, como `API_V1_STR` (padrão `/api/v1`) e `BACKEND_CORS_ORIGINS`.

## Instalação

1. Clone o repositório

```powershell
git clone https://github.com/vitorhugo-dev-1/AI-dungeon-master-back.git .
```

2. Crie e ative um ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3. Instale dependências

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4. Crie o arquivo `.env` (copie do `.env.example` e preencha com seus valores).

## Executando a aplicação (desenvolvimento)

Inicie o servidor com Uvicorn (com auto-reload para desenvolvimento):

```powershell
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Endpoints úteis:

- Documentação interativa (Swagger): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000{API_V1_STR}/openapi.json  (por padrão `/api/v1/openapi.json`)

Observação: o `openapi_url` foi configurado em `app.py` como `f"{settings.API_V1_STR}/openapi.json"`.

## Banco de dados

O projeto usa MongoDB. Garanta que o serviço esteja ativo e que `MONGO_CONNECTION_STRING` aponte para ele. Ao iniciar a aplicação, o Beanie deve registrar as seguintes collections caso ainda não existam:

- `User`
- `Personagem`
- `Campanha`

## Envio de e-mail

As configurações estão em `core/config.py` usando `fastapi-mail` (ConnectionConfig). Para Gmail use uma senha de app (App Password) e configure `MAIL_SERVER`/`MAIL_PORT` conforme seu provedor.

## Desenvolvimento e notas internas

- Autenticação: o projeto usa JWT (`python-jose`) para geração e validação de tokens.
- WebSockets: handlers e serviços para comunicação em tempo real estão em `api/api_v1/handlers/websocket.py` e `services/websocket_service.py`.
- Inicialização/`lifespan`: a função `lifespan` em `app.py` inicializa a conexão com o MongoDB e injeta os modelos Beanie.

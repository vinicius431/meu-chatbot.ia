from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from .database import engine
from . import models

app = FastAPI(
    title="Chatbot API - Groq & FastAPI",
    version="1.0.0",
    description="Backend de alta performance para chatbot com IA integrada."
)

# Configuração de CORS (Permite que o React em localhost:5173 consuma esta API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas da aplicação
app.include_router(chat.router)

@app.get("/")
def read_root():
    """Rota raiz para verificar se o servidor está online."""
    return {"status": "online", "message": "API de atendimento WhatsApp a operar com SQLite!"}

# Cria as tabelas no SQLite se elas ainda não existirem
models.Base.metadata.create_all(bind=engine)
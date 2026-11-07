from fastapi import APIRouter, HTTPException
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.groq_service import groq_service

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
def chat_with_ai(payload: ChatRequest):
    """
    Recebe a mensagem do utilizador, envia para o Groq através do serviço
    e retorna a resposta formatada em JSON.
    """
    try:
        ai_reply = groq_service.get_chat_response(payload.message)
        return ChatResponse(response=ai_reply)
    
    except RuntimeError as re:
        # Erro tratado vindo do serviço (ex: indisponibilidade da API)
        raise HTTPException(status_code=503, detail=str(re))
    
    except Exception as e:
        # Erro genérico inesperado
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")
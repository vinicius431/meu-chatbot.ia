from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.groq_service import groq_service
from app.database import get_db
from app import models

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
def chat_with_ai(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Recebe a mensagem, gere o lead, busca o histórico da BD, 
    envia o contexto para a Groq e persiste a nova resposta.
    """
    try:
        phone = getattr(payload, "phone_number", "default_client")
        lead_name = getattr(payload, "name", "Cliente WhatsApp")

        # 1. Verificar ou criar o lead na base de dados
        lead = db.query(models.LeadModel).filter(models.LeadModel.phone_number == phone).first()
        if not lead:
            lead = models.LeadModel(phone_number=phone, name=lead_name, status="novo")
            db.add(lead)
            db.commit()
            db.refresh(lead)

        # 2. Guardar a mensagem atual enviada pelo utilizador na BD
        user_msg = models.MessageModel(
            lead_id=lead.id,
            sender="user",
            content=payload.message
        )
        db.add(user_msg)
        db.commit()

        # 3. Buscar o histórico recente de mensagens deste lead na BD (ex: últimas 10 mensagens)
        past_messages = db.query(models.MessageModel)\
            .filter(models.MessageModel.lead_id == lead.id)\
            .order_by(models.MessageModel.timestamp.desc())\
            .limit(10)\
            .all()
        
        # Inverter para ordem cronológica (da mais antiga para a mais recente)
        past_messages.reverse()

        # Converter o histórico da BD para o formato esperado pelo serviço (role/content)
        formatted_history = [
            {"role": msg.sender, "content": msg.content}
            for msg in past_messages
        ]

        # 4. Obter a resposta da IA passando o histórico completo com o contexto
        ai_reply = groq_service.get_chat_response(formatted_history)

        # 5. Guardar a resposta da IA na BD
        assistant_msg = models.MessageModel(
            lead_id=lead.id,
            sender="assistant",
            content=ai_reply
        )
        db.add(assistant_msg)
        db.commit()

        return ChatResponse(response=ai_reply)
    
    except RuntimeError as re:
        db.rollback()
        raise HTTPException(status_code=503, detail=str(re))
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")
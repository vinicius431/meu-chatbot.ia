from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class LeadModel(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False) # Número de WhatsApp
    name = Column(String, nullable=True)
    status = Column(String, default="novo") # ex: novo, qualificado, agendado
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relação com as mensagens
    messages = relationship("MessageModel", back_populates="lead")

class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    sender = Column(String, nullable=False) # 'user' (cliente) ou 'assistant' (IA/humano)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relação de volta para o lead
    lead = relationship("LeadModel", back_populates="messages")
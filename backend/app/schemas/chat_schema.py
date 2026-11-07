from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="A mensagem enviada pelo utilizador.")

class ChatResponse(BaseModel):
    response: str = Field(..., description="A resposta gerada pelo modelo de IA do Groq.")
    
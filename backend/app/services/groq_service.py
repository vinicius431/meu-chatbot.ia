from openai import OpenAI
from app.config import settings

class GroqService:
    def __init__(self):
        # Inicializamos o cliente da OpenAI apontando para a base URL do Groq
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        # Mantemos rigorosamente o modelo que sabes que funciona no teu ambiente
        self.model = "openai/gpt-oss-20b"

    def get_chat_response(self, messages_history: list) -> str:
        """
        Envia o histórico completo de mensagens para a API do Groq e retorna a resposta da IA,
        mantendo o contexto conversacional sem perder a estrutura original.
        """
        try:
            # System prompt inicial preservando a tua diretriz de assistente prestativo
            system_prompt = {
                "role": "system", 
                "content": "És um assistente virtual especialista e prestativo. Lembra-te do nome do cliente e do contexto das mensagens anteriores."
            }
            
            # Combinamos o system prompt com o histórico que o chat.py foi buscar à base de dados
            messages = [system_prompt] + messages_history

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )
            return response.choices[0].message.content
        
        except Exception as e:
            # Vamos imprimir o erro real no terminal do uvicorn
            print(f"ERRO REAL DA GROQ: {str(e)}")
            raise RuntimeError(f"Erro real: {str(e)}")

# Instância global do serviço
groq_service = GroqService()
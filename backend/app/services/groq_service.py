from openai import OpenAI
from app.config import settings

class GroqService:
    def __init__(self):
        # Inicializamos o cliente da OpenAI apontando para a base URL do Groq
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = "openai/gpt-oss-20b"

    def get_chat_response(self, user_message: str) -> str:
        """
        Envia a mensagem do utilizador para a API do Groq e retorna a resposta da IA.
        Inclui tratamento básico de exceções para resiliência.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "És um assistente virtual especialista e prestativo."},
                    {"role": "user", "content": user_message}
                ],
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

import os
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env localizado na raiz do projeto
load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile") # Modelo padrão de alta performance do Groq

settings = Settings()

# Validação básica de segurança na inicialização
if not settings.GROQ_API_KEY:
    print("⚠️ AVISO: GROQ_API_KEY não encontrada no ficheiro .env!")
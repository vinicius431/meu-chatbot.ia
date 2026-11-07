from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define o ficheiro local do SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./chatbot.db"

# Cria o motor de ligação (connect_args é necessário para o SQLite no FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fábrica de sessões para interagir com a BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os nossos modelos de tabelas
Base = declarative_base()

# Dependência para obter a sessão da BD em cada rota do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
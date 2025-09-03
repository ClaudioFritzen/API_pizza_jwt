from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Pega a URL do banco
DATABASE_URL = os.getenv("DATABASE_URL")

# Configura SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Teste simples
def testar_conexao():
    try:
        with engine.connect() as conn:
            print("✅ Conexão bem-sucedida com o PostgreSQL!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")

if __name__ == "__main__":
    testar_conexao()

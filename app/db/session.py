from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine


# Define a base declarativa para os modelos
class Base(DeclarativeBase):
    pass


# Cria a engine do banco de dados
DATABASE_URL = "sqlite:///./real.db"  # Pode ser movido para config.py futuramente
DATABASE_URL_TEST = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=False)

# Cria a fábrica de sessões
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Função de dependência para FastAPI
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from app.config import DATABASE_URL


# Define a base declarativa para os modelos
class Base(DeclarativeBase):
    pass


# Cria a engine do banco de dados
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

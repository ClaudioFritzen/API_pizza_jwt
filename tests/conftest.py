# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.db.tests_db import TestingSessionLocal
from app.db.session import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app

from dotenv import load_dotenv
import os

load_dotenv()

## Configuração do banco de dados de teste
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")
# Engine e sessão de teste
engine_test = create_engine(DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)



## Criar a tabela e exclui 
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    print("🔧 Criando tabelas para testes...")
    Base.metadata.create_all(bind=engine_test)
    yield
    print("\n🔧 Todos os testes foram executados.")
    Base.metadata.drop_all(bind=engine_test)
    print("🧹 Removendo tabelas de testes...")

# Limpeza entre testes
@pytest.fixture(autouse=True)
def clean_database():
    session = TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()


# 🔁 1. Override da dependência do banco
@pytest.fixture
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🧪 2. Cliente com override ativo
@pytest.fixture
def cliente(override_get_db):
    app.dependency_overrides[get_db] = lambda: override_get_db
    return TestClient(app)


# 🛠️ 3. Garantir que o override está sempre ativo
@pytest.fixture(autouse=True)
def configurar_db(monkeypatch, override_get_db):
    monkeypatch.setattr("app.db.session.get_db", lambda: override_get_db)

# 🧼 4. Sessão de teste reutilizável
@pytest.fixture
def test_db_sessao(override_get_db):
    return override_get_db
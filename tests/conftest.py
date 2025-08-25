# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.tests_db import TestingSessionLocal
from app.db.session import get_db


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


# 🧼 3. Sessão de teste reutilizável
@pytest.fixture
def test_db_sessao(override_get_db):
    return override_get_db


# 🛠️ 4. Garantir que o override está sempre ativo
@pytest.fixture(autouse=True)
def configurar_db(monkeypatch, override_get_db):
    monkeypatch.setattr("app.db.session.get_db", lambda: override_get_db)

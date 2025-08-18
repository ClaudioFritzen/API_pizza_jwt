# conftest.py

import pytest
import os
from urllib.parse import urlparse
from fastapi.testclient import TestClient
from sqlalchemy import inspect

from app.main import app
from app.db.session import Base, DATABASE_URL_TEST, engine, Session, get_db
from app.models.models import Usuario  # garante que as tabelas sejam registradas

# ✅ Exportável: caminho do banco de testes
parsed = urlparse(DATABASE_URL_TEST)
TEST_DB_PATH = parsed.path.lstrip('/')  # agora pode ser importado

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    print("🔧 Criando test.db e tabelas...")
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert tables, "Nenhuma tabela foi criada no banco de testes."
    yield

    print("🧹 Removendo test.db...")
    engine.dispose()
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
        print("✅ test.db removido com sucesso.")
    else:
        print("⚠️ test.db não encontrado para remoção.")

@pytest.fixture(scope="session")
def client():
    def override_get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

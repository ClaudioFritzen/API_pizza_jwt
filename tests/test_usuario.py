from fastapi.testclient import TestClient
from app.db.session import Base, get_db
from app.main import app
from app.db.tests_db import TestingSessionLocal, engine_test
from app.models.models import Usuario
import pytest
from app.schemas.schema_usuario import UsuarioSchema

cliente = TestClient(app)


# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine_test)


# sobre escreve a sessão de teste

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def limpar_usuarios():
    db = TestingSessionLocal()
    db.query(Usuario).delete()
    db.commit()
    db.close()


class TestUsuario:

    def test_usuario_valido(limpar_usuarios):
        payload = {
            "email": "claudiosilva@pizza.com",
            "nome": "Claudio",
            "senha": "senha123",
            "ativo": True,
            "admin": False
        }

        response = cliente.post("/auth/criar_conta/", json=payload)

        assert response.status_code in [201, 200]

        data = response.json()
        print("📥 Resposta recebida:", data)

        # verificar se os campos estao presentes
        
        assert "id" in data
        assert data["email"] == payload["email"]
        assert data["nome"] == payload["nome"]
           # Se o schema de resposta incluir 'ativo' e 'admin', também valide:
        if "ativo" in data:
            assert data["ativo"] == payload["ativo"]
        if "admin" in data:
            assert data["admin"] == payload["admin"]


    def test_email_unico(limpar_usuarios):
        payload = {
            "nome": "usuario unico",
            "email": "usuario_unico@teste.com",
            "senha": "senha123"
        }

        print("🚀 Enviando POST para /auth/criar_conta/")
        response = cliente.post("/auth/criar_conta/", json=payload)
        data = response.json()
        print("📥 Resposta recebida:", data)

        assert response.status_code in [201, 200]
        assert data["email"] == "usuario_unico@teste.com"
        assert data["nome"] == "usuario unico"
        assert data["ativo"] is True
        assert data["admin"] is False

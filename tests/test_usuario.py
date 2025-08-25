from app.main import app
from app.db.tests_db import TestingSessionLocal, engine_test
from app.models.models import Usuario
import pytest
from app.schemas.schema_usuario import UsuarioSchema
from tests.conftest import cliente, test_db_sessao



@pytest.fixture(autouse=True)
def limpar_usuarios():
    db = TestingSessionLocal()
    db.query(Usuario).delete()
    db.commit()
    db.close()

# TDD com usuario admin para criar as contas



def criar_usuario_admin(test_db_sessao):
    from app.models.models import Usuario

    admin = Usuario(
        email="admin@pizza.com",
        nome="Admin",
        senha="senha123",
        ativo=True,
        admin=True
    )
    admin.set_password("senha123")
    test_db_sessao.add(admin)
    test_db_sessao.commit()
    test_db_sessao.refresh(admin)

def test_criar_usuario_admin(cliente, test_db_sessao):
    criar_usuario_admin(test_db_sessao)

def test_login_admin(cliente, test_db_sessao):
    # cria o admin no db
    test_criar_usuario_admin(cliente, test_db_sessao)

    # Faz o login com email e senha
    response = cliente.post("/auth/login/", json={
        "email": "admin@pizza.com",
        "senha": "senha123"
    })

    print(f"🔐 Status: {response.status_code}")
    print(f"🔐 Resposta: {response.json()}")

    # Verifica se o token foi gerado
    assert response.status_code == 200
    assert "access_token" in response.json()

""" 
def test_criar_conta_com_admin(self, cliente, test_db_sessao):
    print("🚀 Iniciando teste de criação de admin")

    # 1️⃣ Criar usuário admin
    test_criar_usuario_admin(test_db_sessao)
    print("✅ Função criar_usuario_admin executada")

    # 2️⃣ Obter token via login
    token = test_obter_token_admin(cliente)
    print(f"🔐 Token recebido: {token}")

    # 3️⃣ Verificar se o token é válido
    assert token is not None
    print("✅ Teste passou: token foi gerado com sucesso")
 """
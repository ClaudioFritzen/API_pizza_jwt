# 📦 Imports principais
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 🧩 Imports da aplicação
from app.main import app
from app.db.tests_db import TestingSessionLocal
from app.db.session import get_db, Base
from app.models.models import Usuario
from app.jwt.jwt_handler import create_token_access_token as criar_token

# 🔧 Função auxiliar para criar admin sem circular import
from tests.usuarios.criar_adm import criar_usuario_admin

# 🌱 Carrega variáveis de ambiente
load_dotenv()

# 🔗 URL do banco de dados de teste
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")

# ⚙️ Criação da engine e sessão de teste
engine_test = create_engine(DATABASE_URL_TEST, connect_args={
                            "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test)

# 🧱 Setup inicial do banco (criação e remoção de tabelas)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    print("🔧 Criando tabelas para testes...")
    Base.metadata.create_all(bind=engine_test)
    yield
    print("\n🔧 Todos os testes foram executados.")
    Base.metadata.drop_all(bind=engine_test)
    print("🧹 Removendo tabelas de testes...")

# 🧼 Limpeza entre testes para garantir isolamento


@pytest.fixture(autouse=True)
def clean_database():
    session = TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()

# 🔁 Override da dependência do banco de dados


@pytest.fixture
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🛠️ Garante que o override do banco está sempre ativo


@pytest.fixture(autouse=True)
def configurar_db(monkeypatch, override_get_db):
    monkeypatch.setattr("app.db.session.get_db", lambda: override_get_db)

# 🔄 Sessão de banco reutilizável para testes


@pytest.fixture
def test_db_sessao(override_get_db):
    return override_get_db

 # 🧪 Cliente de teste com dependência de banco sobrescrita


@pytest.fixture
def cliente(override_get_db):
    app.dependency_overrides[get_db] = lambda: override_get_db
    return TestClient(app) 

# 🔐 Gera token JWT para usuário comum (não-admin)


@pytest.fixture
def token_usuario_comum(test_db_sessao):
    usuario = test_db_sessao.query(Usuario).filter_by(
        email="usuario@pizza.com").first()
    if not usuario:
        usuario = Usuario(email="usuario@pizza.com",
                          senha="senha_segura", admin=False, nome="Usuário Comum")
        test_db_sessao.add(usuario)
        test_db_sessao.commit()
    access_token, refresh_token = criar_token(usuario.id)
    return access_token # Não retornar o refresh token aqui vai dar erro 401, mas é pq esta sendo passado os dois tokens no header

# 🔐 Gera token JWT para usuário administrador


@pytest.fixture
def token_admin(test_db_sessao):
    criar_usuario_admin()  # Cria admin se não existir
    email_admin = os.getenv("ADM_USER")
    usuario = test_db_sessao.query(
        Usuario).filter_by(email=email_admin).first()
    # retornar o token JWT com print
    access_token, refresh_token = criar_token(usuario.id)
    print(f"🔑 Token admin gerado: {access_token}")
    return access_token

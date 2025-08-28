from app.main import app
from app.db.tests_db import TestingSessionLocal, engine_test
from app.models.models import Usuario
import pytest
from app.schemas.schema_usuario import UsuarioSchema
from tests.conftest import cliente, test_db_sessao
from dotenv import load_dotenv
import os

load_dotenv()

def criar_usuario_admin(test_db_sessao):
    db = TestingSessionLocal()
    email = os.getenv("ADM_USER")
    senha = os.getenv("ADM_PASSWORD")

    if not email or not senha:
        raise ValueError("As variáveis de ambiente ADM_USER e ADM_PASSWORD devem estar definidas.")

    admin_existente = db.query(Usuario).filter_by(email=email).first()

    if admin_existente:
        print("Admin já existe no banco de dados.")
        db.close()
        return
    
    novo_admin = Usuario(
        email=email,
        nome="Admin",
        senha=senha,
        ativo=True,
        admin=True
    )
    novo_admin.set_password(senha)
    db.add(novo_admin)
    db.commit()
    db.refresh(novo_admin)
    db.close()
    print(f"Admin criado: {novo_admin.email}")


def test_criar_usuario_admin(cliente, test_db_sessao):
    criar_usuario_admin(test_db_sessao)
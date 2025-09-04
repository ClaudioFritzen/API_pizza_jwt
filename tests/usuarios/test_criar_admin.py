# tests/usuarios/test_admin_setup.py
from app.models.models import Usuario
from tests.usuarios.criar_adm import criar_usuario_admin
import os

def test_criar_usuario_admin(test_db_sessao):
    criar_usuario_admin()
    email_admin = os.getenv("ADM_USER")
    usuario = test_db_sessao.query(Usuario).filter_by(email=email_admin).first()
    print(f"🔍 Usuario admin criado: {usuario}")
    assert usuario is not None
    assert usuario.admin is True
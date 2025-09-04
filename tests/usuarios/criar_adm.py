# tests/usuarios/test_criar_admin.py

from app.db.tests_db import TestingSessionLocal
from app.models.models import Usuario
import os

def criar_usuario_admin():
    db = TestingSessionLocal()
    email = os.getenv("ADM_USER")
    senha = os.getenv("ADM_PASSWORD")

    if not email or not senha:
        raise ValueError("ADM_USER e ADM_PASSWORD devem estar definidos.")

    admin_existente = db.query(Usuario).filter_by(email=email).first()
    if admin_existente:
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

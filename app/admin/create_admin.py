from app.models.models import Usuario
from app.db.session import Session
from app.config import ADM_PASSWORD, ADM_USER, crypt_context

ADM_EMAIL = ADM_USER
ADM_PASSWORD = ADM_PASSWORD


def create_initial_admin():
    db = Session()

    try:
        # Verifica se já existe um admin com esse email
        existing_admin = db.query(Usuario).filter(Usuario.email == ADM_EMAIL).first()
        if existing_admin:
            print("Admin já existe.")
            return
        hashed_password = crypt_context.hash(ADM_PASSWORD)
        admin_user = Usuario(
            nome = "Admin Inicial",
            email = ADM_EMAIL,
            senha = hashed_password,
            admin = True,
            ativo = True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        return admin_user
    except Exception as e:
        print(f"Erro ao criar admin: {e}")
        db.rollback()
        return None
    finally:
        db.close()
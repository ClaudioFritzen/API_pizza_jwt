""" from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base

# Configuração do banco de dados de teste
DATABASE_URL_TEST = "sqlite:///./test.db"

# Engine e sessão de teste
engine_test = create_engine(DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# Cria as tabelas no banco de dados de teste
Base.metadata.create_all(bind=engine_test)
 """

def test_db_funciona(cliente, test_db_sessao):
    from app.models.models import Usuario

    novo = Usuario(email="teste@teste.com", senha="123", eh_admin=False)
    test_db_sessao.add(novo)
    test_db_sessao.commit()

    resultado = test_db_sessao.query(Usuario).filter_by(email="teste@teste.com").first()
    print(f"👀 Usuario criado: {resultado.email}")
    assert resultado is not None

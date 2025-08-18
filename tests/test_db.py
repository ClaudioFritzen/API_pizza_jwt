from tests.conftest import TEST_DB_PATH
from sqlalchemy import inspect
from app.db.session import engine
import os

def test_db_setup():
    print("🧪 Verificando se o banco foi criado e contém tabelas.")
    assert os.path.exists(TEST_DB_PATH), "Arquivo test.db não foi criado."

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert len(tables) > 0, "Nenhuma tabela foi criada no banco de testes."

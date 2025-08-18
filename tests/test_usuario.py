from fastapi.testclient import TestClient
from app.main import app

cliente = TestClient(app)

def test_usuario_valido():
    payload = {
        "nome": "Claudio",
        "email": "claudiosilva@gmail.com",
        "senha": "senha123",
    }

    response = cliente.post("/usuarios/", json=payload)

    assert response.status_code == 201
    assert response.json()["nome"] == "Claudio"
    assert response.json()["email"] == "claudiosilva@gmail.com"


def test_usuario_salvo_em_testdb():
    payload = {
        "nome": "Claudio",
        "email": "claudio@teste.com",
        "senha": "senha123"
    }

    print("🚀 Enviando POST para /usuarios/")
    response = cliente.post("/usuarios/", json=payload)

    print("📥 Resposta recebida:", response.json())
    assert response.status_code == 201
    assert response.json()["email"] == "claudio@teste.com"

from urllib import response
from tests.usuarios.test_criar_admin import criar_usuario_admin
from dotenv import load_dotenv
import os
import pytest
from app.models.models import Usuario
load_dotenv()


def test_criar_usuario_comum__como_administrador(cliente, test_db_sessao):
    criar_usuario_admin(test_db_sessao)
    email = os.getenv("ADM_USER")
    senha = os.getenv("ADM_PASSWORD")
    # login para obter o token
    response = cliente.post("/auth/login/", json={ 
        "email": email,
        "senha": senha
    })

    # Criar novo usuario
    response = cliente.post("/auth/criar_conta", json={
        "email": "test_05_como_adm@pizza.com",
        "nome": "Usuario Criado como ADM",
        "senha": "novotest",
        "admin": True,
        "ativo": True
    },
        headers={"Authorization": f"Bearer {response.json()['access_token']}"}
    )
    assert response.status_code == 201



def test_criar_usuario_comum(cliente, test_db_sessao):
    criar_usuario_admin(test_db_sessao)
    email = os.getenv("ADM_USER")
    senha = os.getenv("ADM_PASSWORD")
    # login para obter o token
    response = cliente.post("/auth/login/", json={ 
        "email": email,
        "senha": senha
    })

    # Criar novo usuario
    response = cliente.post("/auth/criar_conta", json={
        "email": "test_06_como_comum@pizza.com",
        "nome": "Usuario Criado como Comum",
        "senha": "novotest",
        "admin": False,
        "ativo": True
    },
        headers={"Authorization": f"Bearer {response.json()['access_token']}"}
    )
    assert response.status_code == 201
    print("Usuario criado com sucesso")
    
#@pytest.mark.xfail(reason="Email duplicado não pode ser cadastrado")
def test_criar_usuario_com_email_existente(cliente, test_db_sessao):
    criar_usuario_admin(test_db_sessao)
    email = os.getenv("ADM_USER")
    senha = os.getenv("ADM_PASSWORD")

    # login para obter o token
    response = cliente.post("/auth/login/", json={ 
        "email": email,
        "senha": senha
    })
    token = response.json()["access_token"]

    # Criar novo usuario
    response = cliente.post("/auth/criar_conta", json={
        "email": "test_07_como_comum@pizza.com",
        "nome": "Email Duplicado",
        "senha": "novotest",
        "admin": False,
        "ativo": True
    },
        #headers={"Authorization": f"Bearer {response.json()['access_token']}"}
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Segundo usuário com mesmo email
    response2 = cliente.post("/auth/criar_conta", json={
        "email": "test_07_como_comum@pizza.com",
        "nome": "Segundo",
        "senha": "teste456",
        "admin": False,
        "ativo": True
    },
        #headers={"Authorization": f"Bearer {response.json()['access_token']}"}
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response2.status_code == 409
    assert response2.json()["detail"] == "Email já cadastrado!"

@pytest.mark.xfail(reason="Usuário comum não pode criar usuario")
def test_criar_usuario_comum(cliente):
    response = cliente.post("/auth/criar_conta", json={
        "email": "test_01@pizza.com",
        "nome": "Usuario Comum tentando criar outro usuario",
        "senha": "novotest",
        "admin": False,
        "ativo": True
    })

    assert response.status_code == 201
    print("Usuario criado com sucesso")
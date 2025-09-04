import pytest
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.jwt.jwt_handler import create_token_access_token, verificar_refresh_token, verificar_token
from app.models.models import Usuario
from fastapi import HTTPException

from app.config import SECRET_KEY, ALGORITHM

SECRET_KEY = SECRET_KEY
ALGORITHM = ALGORITHM

class FakeSession:
    def query(self, model):
        class Query:
            def filter(self, condition):
                class Result:
                    def first(self):
                        return Usuario(id=1, email="teste@teste.com")  # simulação
                return Result()
        return Query()
    
class FakeSessionSemUsuario:
    def query(self, model):
        class Query:
            def filter(self, condition):
                class Result:
                    def first(self):
                        return None
                return Result()
        return Query()
    

def test_create_token_access_token():
    usuario_id = 123
    access_token, refresh_token = create_token_access_token(usuario_id)

    access_payload  = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    refresh_payload  = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

    ## verifica campos obrigatorios
    assert access_payload["sub"] == str(usuario_id)
    assert "exp" in access_payload
    assert "iat" in access_payload
    
    
    assert refresh_payload["sub"] == str(usuario_id)
    assert "exp" in refresh_payload
    assert "iat" in refresh_payload

    # verifica se o resfresh é maior que o access
    access_exp = datetime.fromtimestamp(access_payload["exp"], tz=timezone.utc)
    refresh_exp = datetime.fromtimestamp(refresh_payload["exp"], tz=timezone.utc)
    assert refresh_exp > access_exp
    print("Refresh token é maior que Access token")

def gerar_token_valido():
    payload = {
        "sub": "1",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def gerar_token_expirado():
    payload = {
        "sub": "1",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
        "iat": datetime.now(timezone.utc) - timedelta(minutes=10)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def test_token_valido():
    token = gerar_token_valido()
    usuario = verificar_refresh_token(token=token, session=FakeSession())
    assert usuario.email == "teste@teste.com"

def test_token_expirado():
    token = gerar_token_expirado()
    with pytest.raises(Exception) as exc:
        verificar_refresh_token(token=token, session=FakeSession())
    assert "Acesso Negado" in str(exc.value)

def test_token_invalido():
    token = "token_invalido"
    with pytest.raises(Exception) as exc:
        verificar_refresh_token(token=token, session=FakeSession())
    assert "Acesso Negado" in str(exc.value)


def test_verficar_token_valiido():
    token = gerar_token_valido()
    usuario = verificar_token(token=token, session=FakeSession())
    assert usuario.email == "teste@teste.com"

def test_token_com_virgula():
    token1 = gerar_token_valido()
    token2 = gerar_token_valido()
    token_com_virgula = f"{token1},{token2}"
    usuario = verificar_token(token=token_com_virgula, session=FakeSession())
    assert usuario.email == "teste@teste.com"


def test_usuario_nao_encontrado():
    token = gerar_token_valido()
    with pytest.raises(HTTPException) as exc:
        verificar_refresh_token(token=token, session=FakeSessionSemUsuario())
    assert "Usuário não encontrado" in str(exc.value)
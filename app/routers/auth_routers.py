from fastapi import APIRouter, Depends, HTTPException, status
from app.models.models import Usuario, Pedido, ItensPedido

from app.schemas.schema_usuario import UsuarioSchema
from app.schemas.schema_login import LoginSchema
from app.schemas.schema_resposta_usuario import UsuarioResponseSchema


## router
from app.db.session import get_db
from sqlalchemy.orm import Session as SessionType
from passlib.context import CryptContext

# jtw e tokens
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, crypt_context
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

# core
from app.core.utils import verificar_token

from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def home():
    """Essa é uma rota padrão"""
    raise HTTPException(status_code=200, detail={"Deu certo": "Essa é uma rota padrão"})


@auth_router.post(
    "/criar_conta",
    response_model=UsuarioResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def criar_conta(usuario_schema: UsuarioSchema, db: SessionType = Depends(get_db), usuario: Usuario = Depends(verificar_token)):

    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado! Somente administradores podem criar contas.")
    
    usuario_existente = (
        db.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado!"
        )

    novo_usuario = Usuario(
        email=usuario_schema.email,
        nome=usuario_schema.nome,
        ativo=usuario_schema.ativo,
        admin=usuario_schema.admin,
    )

    novo_usuario.set_password(usuario_schema.senha)  # 🔐 Criptografando a senha
    db.add(novo_usuario)
    db.commit()

    db.refresh(novo_usuario)
    return novo_usuario


# login -> email e senha -> token jwt


def criar_token(
    usuario_id, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
):
    """Função para criar um token JWT"""
    data_expiracao = datetime.now(timezone.utc) + duracao_token

    # id_usuario
    # data_expiracao
    # refreshtoken
    dict_info = {
        "sub": str(usuario_id),
        "exp": data_expiracao,
        "iat": datetime.now(timezone.utc),
    }
    jwt_codificado = jwt.encode(dict_info, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_codificado


## Função para autenticar o usuário
def autenticar_usuario(email, senha, db):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        return False
    elif not crypt_context.verify(senha, usuario.senha):
        return False

    return usuario


@auth_router.post("/login")
async def login(login_schema: LoginSchema, db: SessionType = Depends(get_db)):

    usuario = autenticar_usuario(login_schema.email, login_schema.senha, db)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos!"
        )

    # Gerar token JWT
    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


### Salvando o token na api de login
@auth_router.post("/login-form")
async def login_form(
    dados_formulario: OAuth2PasswordRequestForm = Depends(),
    db: SessionType = Depends(get_db),
):

    usuario = autenticar_usuario(
        dados_formulario.username, dados_formulario.password, db
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos!"
        )

    access_token = criar_token(usuario.id)
    return {"access_token": access_token, "token_type": "bearer"}


# rota se tiver logado


@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)

    return {"access_token": access_token, "token_type": "bearer"}


# delete account by id
@auth_router.delete("/delete/{user_id}")
async def delete_account_by_id(user_id: int, db: SessionType = Depends(get_db), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado! Somente administradores podem deletar contas.")

    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    db.delete(usuario)
    db.commit()
    return {"detail": "Conta deletada com sucesso"}


@auth_router.get("/usuarios")
async def listar_usuarios(db: SessionType = Depends(get_db), usuario: Usuario = Depends(verificar_token)):

    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado! Você não tem permissão para acessar essa rota.")
    
    usuarios = db.query(Usuario).all()
    return usuarios
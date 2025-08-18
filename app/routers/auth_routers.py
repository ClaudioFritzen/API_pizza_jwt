from fastapi import APIRouter, Depends, HTTPException, status
from app.models.models import Usuario, Pedido, ItensPedido

from app.schemas.schema_usuario import UsuarioSchema
from app.schemas.schema_resposta_usuario import UsuarioResponseSchema

## router
from app.db.session import get_db
from sqlalchemy.orm import Session as SessionType 


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """ Essa é uma rota padrão"""
    raise HTTPException(status_code=200, detail={"Deu certo": "Essa é uma rota padrão"})


@auth_router.post("/criar_conta", response_model=UsuarioResponseSchema, status_code=status.HTTP_201_CREATED)
async def criar_conta(usuario_schema: UsuarioSchema, db: SessionType = Depends(get_db)):

    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado!"
        )

    novo_usuario = Usuario(
        email=usuario_schema.email,
        nome=usuario_schema.nome,
        ativo=usuario_schema.ativo,
        admin=usuario_schema.admin
    )

    novo_usuario.set_password(usuario_schema.senha)  # 🔐 Criptografando a senha
    db.add(novo_usuario)
    db.commit()

    db.refresh(novo_usuario)
    return novo_usuario
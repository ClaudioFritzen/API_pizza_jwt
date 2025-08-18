from fastapi import APIRouter, Depends, HTTPException
from app.models.models import Usuario, Pedido, ItensPedido

from app.schemas.schema_usuario import UsuarioSchema

## router
from app.db.session import get_db
from sqlalchemy.orm import Session as SessionType 


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """ Essa é uma rota padrão"""
    raise HTTPException(status_code=200, detail={"Deu certo": "Essa é uma rota padrão"})


@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, db: SessionType = Depends(get_db)):

    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

    if usuario_existente:
        raise HTTPException(status_code=409, detail={"Erro": "email ja cadastrado!"})

    novo_usuario = Usuario(email=usuario_schema.email, nome=usuario_schema.nome)
    novo_usuario.set_password(usuario_schema.senha)  # 🔐 Criptografando a senha
    db.add(novo_usuario)
    db.commit()
    return {"message": f"Conta criada com sucesso {usuario_schema.email}"}


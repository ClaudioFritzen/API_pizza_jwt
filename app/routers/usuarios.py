from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

class Usuario(BaseModel):
    nome: str
    email: str
    senha: str

@router.post("/usuarios/", status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario: Usuario):
    # Lógica para criar o usuário
    return {
        "nome": usuario.nome,
        "email": usuario.email,
    }

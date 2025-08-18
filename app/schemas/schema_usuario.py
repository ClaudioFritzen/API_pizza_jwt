from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):


    email: str
    nome: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

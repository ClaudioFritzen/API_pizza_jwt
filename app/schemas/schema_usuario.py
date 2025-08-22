from pydantic import BaseModel
from typing import Optional
from pydantic import ConfigDict


class UsuarioSchema(BaseModel):

    email: str
    nome: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

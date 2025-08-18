from pydantic import BaseModel, ConfigDict
from typing import Optional

class UsuarioResponseSchema(BaseModel):
    id: int
    email: str
    nome: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

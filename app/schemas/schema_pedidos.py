from pydantic import BaseModel, validator
from pydantic import ConfigDict


class PedidoSchema(BaseModel):
    usuario_id: int

    @validator("usuario_id")
    def validar_usuario_id(cls, v):
        if v <= 0:
            raise ValueError("O ID do usuário deve ser um número positivo.")
        return v
    
    model_config = ConfigDict(from_attributes=True)

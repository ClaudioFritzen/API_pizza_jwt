from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic import ConfigDict


class PedidoSchema(BaseModel):
    usuario_id: int

    model_config = ConfigDict(from_attributes=True)

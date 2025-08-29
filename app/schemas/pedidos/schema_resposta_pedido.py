from pydantic import BaseModel
from pydantic import ConfigDict
from typing import List
from app.schemas.pedidos.schema_pedido_item import ItemPedidoSchema

class RespostaPedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]
    model_config = ConfigDict(from_attributes=True)
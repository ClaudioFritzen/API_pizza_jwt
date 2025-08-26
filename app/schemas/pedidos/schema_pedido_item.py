from pydantic import BaseModel
from pydantic import ConfigDict

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    preco_unitario: float
    tamanho: str

    model_config = ConfigDict(from_attributes=True)


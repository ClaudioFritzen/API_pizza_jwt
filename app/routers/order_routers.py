from fastapi import APIRouter, Depends, HTTPException

from app.models.models import Pedido

## router
from app.db.session import get_db
from sqlalchemy.orm import Session as SessionType

from app.schemas.schema_pedidos import PedidoSchema

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@order_router.post("/")
async def pedidos():
    """
    Essa é a rota padrao de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação.

    """
    return {"message": "Você acessou a rota pedidos"}


@order_router.post("/criar_pedido")
async def criar_pedido(pedido_schema: PedidoSchema, db: SessionType = Depends(get_db)):
    """
    Essa é a rota para criar um novo pedido.
    """
    if not pedido_schema.usuario_id:
        raise HTTPException(status_code=400, detail="ID do usuário é obrigatório")

    novo_pedido = Pedido(**pedido_schema.dict())

    db.add(novo_pedido)
    db.commit()
    return {
        "message": f"Pedido criado com sucesso para o usuário {pedido_schema.usuario_id}"
    }

from fastapi import APIRouter, Depends, HTTPException

from app.models.models import Pedido

## router
from app.db.session import get_db
from sqlalchemy.orm import Session as SessionType

from app.schemas.schema_pedidos import PedidoSchema
from app.core.utils import verificar_token
from app.models.models import Usuario
order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])


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

@order_router.post("pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, db: SessionType = Depends(get_db), usuario: Usuario = Depends(verificar_token)):

    ## usuario.admin = True
    # usuario.id = pedido.usuario_id

    pedido = db.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.status == "cancelado":
        raise HTTPException(status_code=400, detail="Pedido já está cancelado")

    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=403, detail="Acesso negado! Você não tem permissão para cancelar este pedido.")

    pedido.status = "cancelado"

    db.commit()
    return {"detail": f"Pedido {pedido.id} cancelado com sucesso",
            "pedido": pedido
    }

# parametro para pegar o usuario
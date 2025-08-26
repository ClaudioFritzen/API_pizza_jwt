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
async def criar_pedido(pedido_schema: PedidoSchema, db: SessionType = Depends(get_db), usuario: Usuario = Depends(verificar_token)):
    """
    Essa é a rota para criar um novo pedido.
    """
    # [x] verificar se o usuario existe
    # [x] pegar o id e ver se existe esse usuario
    # [x] vericar se quem fez o pedido é adm ou é igual id dele
    # [x] Vamos burcar no db se o usuario existe

    usuario_existe = db.query(Usuario).filter(Usuario.id == pedido_schema.usuario_id).first()

    if not usuario_existe:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    ## Verifica se o id de quem esta fazendo a solicitacao do pedido é o mesmo que o id do usuario
    if not usuario.admin and usuario.id != pedido_schema.usuario_id:
        raise HTTPException(status_code=403, detail="Acesso negado! Você não tem permissão para criar este pedido.")

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

@order_router.get("/listar_pedidos")
async def listar_pedidos(db: SessionType = Depends(get_db), usuario: Usuario = Depends(verificar_token)):
    """
    Essa é a rota para listar todos os pedidos.
    """
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado! Apenas administradores podem listar todos os pedidos.")
    pedidos = db.query(Pedido).all()
    return {"pedidos": pedidos}
from fastapi import APIRouter

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.post("/")
async def create_order(item_id: int, quantity: int, nome: str):
    return {"item_id": item_id, "quantity": quantity, "nome": nome}

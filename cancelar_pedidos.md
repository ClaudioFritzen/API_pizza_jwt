

# Como vai funcionar isso!!

## Temos que ter um usuario admin, e um pedido que status != cancelado


Para cancelar o pedido a pessoa que esta tentando cancelar deve ser adm ou ser dona do proprio pedido


primeira coisa que iremos fazer,

buscar o pedido

fazer as validações 

    se o pedido existe
    se o pedido já não esta cancelado
    se a pessoa é admin ou dona do pedido

mas antes temos que passar no inicio da função 

    usuario: Usuario = Depends(verificar_token)

    esse parametro ira pegar quem mandou a requisição, e assim conseguiremos fazer as verificações 




# 🚫 Cancelamento de Pedido com Controle de Acesso

Este documento descreve a lógica de autorização para o endpoint de cancelamento de pedidos na API FastAPI. O objetivo é garantir que apenas usuários autorizados possam cancelar pedidos, respeitando os níveis de acesso definidos.

---

## 🔧 Endpoint

```http
POST /pedido/cancelar/{id_pedido}

🔐 Regras de Acesso
Administradores (usuario.admin = True) podem cancelar qualquer pedido.

Usuários comuns só podem cancelar seus próprios pedidos (usuario.id == pedido.usuario_id).

Se o pedido já estiver cancelado, retorna erro 400.

Se o pedido não existir, retorna erro 404.

🧠 Lógica de Verificação
python
if not usuario.admin and usuario.id != pedido.usuario_id:
    raise HTTPException(
        status_code=403,
        detail="Acesso negado! Você não tem permissão para cancelar este pedido."
    )
Essa verificação garante que apenas o dono do pedido ou um admin possa realizar o cancelamento.

✅ Resposta de Sucesso
json
{
  "detail": "Pedido 123 cancelado com sucesso",
  "pedido": {
    "id": 123,
    "status": "cancelado",
    ...
  }
}
⚠️ Possíveis Erros
Código	Descrição
404	Pedido não encontrado
400	Pedido já está cancelado
403	Acesso negado (usuário não autorizado)
🛠️ Exemplo de Implementação
python
@order_router.post("pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
    id_pedido: int,
    db: SessionType = Depends(get_db),
    usuario: Usuario = Depends(verificar_token)
):
    pedido = db.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.status == "cancelado":
        raise HTTPException(status_code=400, detail="Pedido já está cancelado")

    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=403, detail="Acesso negado! Você não tem permissão para cancelar este pedido.")

    pedido.status = "cancelado"
    db.commit()

    return {
        "detail": f"Pedido {id_pedido} cancelado com sucesso",
        "pedido": pedido
    }
📌 Observações
A verificação de acesso é feita diretamente na rota, mas pode ser extraída para uma função de autorização separada para reutilização.

O campo admin deve estar presente no modelo de usuário e ser incluído no token JWT para facilitar a verificação.
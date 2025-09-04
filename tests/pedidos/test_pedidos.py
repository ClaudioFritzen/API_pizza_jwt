from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Usuario, Pedido, ItensPedido
import pytest


client = TestClient(app)

@pytest.fixture
def criar_pedidos_e_itens_pedidos(test_db_sessao, token_usuario_comum, token_admin):
    # Buscar os usuários já existentes
    usuario_comum = test_db_sessao.query(Usuario).filter_by(email="usuario@pizza.com").first()

    usuario_admin = test_db_sessao.query(Usuario).filter_by(email="claudiosilva@gmail.com").first()

    if not usuario_comum or not usuario_admin:
        raise ValueError("❌ Usuários não encontrados no banco. Certifique-se de que foram criados antes.")

    # Criar pedido para o usuário comum
    pedido_comum = Pedido(usuario_id=usuario_comum.id)
    item_comum = ItensPedido(
        pedido=pedido_comum,
        sabor="Margherita",
        quantidade=2,
        preco_unitario=12.5,
        tamanho="Média"
    )

    # Criar pedido para o admin
    pedido_admin = Pedido(usuario_id=usuario_admin.id)
    item_admin = ItensPedido(
        pedido=pedido_admin,
        sabor="Pepperoni",
        quantidade=1,
        preco_unitario=15.0,
        tamanho="Grande"
    )

    # Persistir no banco
    test_db_sessao.add_all([pedido_comum, item_comum, pedido_admin, item_admin])
    test_db_sessao.commit()
    return {
        "usuario_comum": usuario_comum,
        "usuario_admin": usuario_admin,
        "pedido_comum": pedido_comum,
        "pedido_admin": pedido_admin,
        "item_comum": item_comum,
        "item_admin": item_admin,
    }


def test_usuario_comum_remove_seu_item(cliente, test_db_sessao, token_usuario_comum, criar_pedidos_e_itens_pedidos):
    item = criar_pedidos_e_itens_pedidos["item_comum"]

    # Remover item
    resposta = cliente.delete(
        f"/pedidos/pedido/remover-item/{item.id}",
        headers={"Authorization": f"Bearer {token_usuario_comum}"}
    )
    assert resposta.status_code in [204, 200] # No Content, utilizado para deleções bem-sucedidas

def test_usuario_comum_nao_remove_item_de_outro_usuario(cliente, test_db_sessao, token_usuario_comum, criar_pedidos_e_itens_pedidos):
    
    item_admin = criar_pedidos_e_itens_pedidos["item_admin"]

    # Usuário comum tenta remover
    resposta = cliente.delete(
        f"/pedidos/pedido/remover-item/{item_admin.id}",
        headers={"Authorization": f"Bearer {token_usuario_comum}"}
    )
    assert resposta.status_code == 403 # Forbidden, pois não tem permissão

def test_admin_remove_item_de_qualquer_usuario(cliente, test_db_sessao, token_usuario_comum, token_admin, criar_pedidos_e_itens_pedidos):

    item_comum = criar_pedidos_e_itens_pedidos["item_comum"]

    # Verifica se o item está vinculado a um pedido
    print(f"🔗 item_comum.pedido_id: {item_comum.pedido_id}")
    assert item_comum.pedido_id is not None, "❌ O item não está vinculado a nenhum pedido"

    # Busca o pedido na sessão de teste
    pedido = test_db_sessao.query(Pedido).filter_by(id=item_comum.pedido_id).first()
    #print(f"🧾 Pedido encontrado: {pedido}")
   # print(f"👤 pedido.usuario_id: {pedido.usuario_id}")

    # Confirma que o pedido pertence a outro usuário (não admin)
    assert pedido.usuario_id != 2, "❌ O pedido pertence ao admin, não a outro usuário"

    # Confirma que o admin tem permissão para excluir
    print(f"✅ Admin está tentando excluir item do pedido do usuário {pedido.usuario_id}")

    resposta = cliente.delete(
        f"/pedidos/pedido/remover-item/{item_comum.id}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    #print(f"📡 Status da resposta: {resposta.status_code}")
    #print(f"📦 Conteúdo da resposta: {resposta.text}")
    # print(f"📦 Conteúdo da resposta: {resposta.json()}")  # ❌ Vai dar erro com 204


    assert resposta.status_code in [200, 204]


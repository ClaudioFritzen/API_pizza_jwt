""" from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Usuario, Pedido, ItensPedido
from app.core.utils import verificar_token

client = TestClient(app)


def test_criar_pedidos_e_itens_pedidos(cliente, test_db_sessao):
    # Buscar os usuários já existentes
    usuario_comum = test_db_sessao.query(Usuario).filter_by(email="usuario@pizza.com").first()
    usuario_admin = test_db_sessao.query(Usuario).filter_by(email="admin@pizza.com").first()

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

    # Acessar os IDs se necessário
    item_comum_id = item_comum.id
    item_admin_id = item_admin.id

    assert item_comum_id is not None
    assert item_admin_id is not None

def test_usuario_comum_remove_seu_item(cliente, test_db_sessao, token_usuario_comum):
    # Criar pedido e item
    usuario = test_db_sessao.query(Usuario).filter_by(email="usuario@pizza.com").first()
    pedido = Pedido(usuario_id=usuario.id)
    test_db_sessao.add(pedido)
    test_db_sessao.flush()

    item = ItensPedido(
        pedido_id=pedido.id,
        sabor="Margherita",
        quantidade=2,
        preco_unitario=12.5,
        tamanho="Média"
    )
    test_db_sessao.add(item)
    test_db_sessao.commit()

    # Remover item
    resposta = cliente.delete(
        f"/itens-pedido/{item.id}",
        headers={"Authorization": f"Bearer {token_usuario_comum}"}
    )
    assert resposta.status_code == 200
def test_usuario_comum_nao_remove_item_de_outro_usuario(cliente, test_db_sessao, token_usuario_comum):
    # Criar pedido para admin
    admin = test_db_sessao.query(Usuario).filter_by(email="admin@pizza.com").first()
    pedido_admin = Pedido(usuario_id=admin.id)
    test_db_sessao.add(pedido_admin)
    test_db_sessao.flush()

    item_admin = ItensPedido(
        pedido_id=pedido_admin.id,
        sabor="Pepperoni",
        quantidade=1,
        preco_unitario=15.0,
        tamanho="Grande"
    )
    test_db_sessao.add(item_admin)
    test_db_sessao.commit()

    # Usuário comum tenta remover
    resposta = cliente.delete(
        f"/itens-pedido/{item_admin.id}",
        headers={"Authorization": f"Bearer {token_usuario_comum}"}
    )
    assert resposta.status_code == 403

def test_admin_remove_item_de_qualquer_usuario(cliente, test_db_sessao, token_admin):
    # Criar pedido para usuário comum
    usuario = test_db_sessao.query(Usuario).filter_by(email="usuario@pizza.com").first()
    pedido = Pedido(usuario_id=usuario.id)
    test_db_sessao.add(pedido)
    test_db_sessao.flush()

    item = ItensPedido(
        pedido_id=pedido.id,
        sabor="Quatro Queijos",
        quantidade=1,
        preco_unitario=13.0,
        tamanho="Grande"
    )
    test_db_sessao.add(item)
    test_db_sessao.commit()

    # Admin remove
    resposta = cliente.delete(
        f"/itens-pedido/{item.id}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert resposta.status_code == 200
 """
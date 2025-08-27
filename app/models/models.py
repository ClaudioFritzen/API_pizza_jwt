from sqlalchemy import Integer, String, Boolean, ForeignKey, Float, Enum, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db.session import Base

from app.config import SECRET_KEY, crypt_context

SECRET_KEY = SECRET_KEY
bcrypt_context = crypt_context

class Usuario(Base):
    __tablename__ = "usuarios"

    ## argumentos
    __table__args__ = (
        Index("ix_usuarios.id", "id"),
        Index("ix_usuarios.email", "email"),
        Index("ix_usuarios.admin", "admin"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def set_password(self, senha_em_texto: str):
        """Criptografa a senha do usuário"""
        self.senha = bcrypt_context.hash(senha_em_texto)

    def verificar_password(self, senha_digitada: str) -> bool:
        """Verifica se a senha informada confere com a senha armazenada"""
        return bcrypt_context.verify(senha_digitada, self.senha)


class Pedido(Base):
    __tablename__ = "pedidos"

    __table_args__ = (
        Index("ix_pedidos.id", "id"),  # order do pedido
        Index("ix_pedidos.status", "status"),
        Index("ix_pedidos.usuario_id", "usuario_id"),  # qual cliente pertence
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    ## mais novo choices type
    status: Mapped[str] = mapped_column(
        Enum("pendente", "finalizado", "cancelado", name="status_enum"),
        nullable=False,
        default="pendente",
    )
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ## Criando uma realation ship
    itens = relationship("ItensPedido", back_populates="pedido", cascade="all, delete")

    def calcular_preco_total(self):
        total = sum(item.preco_unitario * item.quantidade for item in self.itens)
        self.preco = total
        return self.preco


class ItensPedido(Base):
    __tablename__ = "itens_pedido"

    __table_args__ = (
        Index("ix_itens_pedido.id", "id"),
        Index("ix_itens_pedido.pedido_id", "pedido_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    sabor: Mapped[str] = mapped_column(String, nullable=False)
    tamanho: Mapped[str] = mapped_column(String, nullable=False)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), nullable=False)
    pedido = relationship("Pedido", back_populates="itens") 


# executar a criacao dos metadados do  seu banco (criar efetivamente o db)

# processo de migração

# alembic lib

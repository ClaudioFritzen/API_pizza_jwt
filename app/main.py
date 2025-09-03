from fastapi import FastAPI
from app.routers.auth_routers import auth_router
from app.routers.order_routers import order_router

from app.admin.create_admin import create_initial_admin
from contextlib import asynccontextmanager
from app.models.models import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando a aplicação...")

    # 🔧 Cria as tabelas no banco
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

    # 👤 Cria o admin inicial
    create_initial_admin()

    yield
    print("Finalizando a aplicação...")


app = FastAPI(
    lifespan=lifespan,
    docs_url="/docs",         # ✅ Isso ativa o Swagger
    redoc_url="/redoc",       # ✅ Isso ativa o ReDoc
    openapi_url="/openapi.json"  # ✅ Isso ativa o schema OpenAPI
)


app.include_router(auth_router)
app.include_router(order_router)
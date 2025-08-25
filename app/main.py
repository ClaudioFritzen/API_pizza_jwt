from fastapi import FastAPI
from app.routers.auth_routers import auth_router
from app.routers.order_routers import order_router

from app.admin.create_admin import create_initial_admin
from contextlib import asynccontextmanager

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando a aplicação...")
    create_initial_admin()
    yield
    print("Finalizando a aplicação...")
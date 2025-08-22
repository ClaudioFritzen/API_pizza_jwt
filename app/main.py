from fastapi import FastAPI
from app.routers.auth_routers import auth_router
from app.routers.order_routers import order_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)


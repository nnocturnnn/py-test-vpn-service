from fastapi import FastAPI
from app.routers import auth, dashboard, proxy

app = FastAPI()

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(proxy.router)
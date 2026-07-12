from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import close_db, connect_db
from app.core.exceptions import register_error_handlers
from app.modules.auth.routes import router as auth_router
from app.modules.items.routes import router as items_router
from app.modules.users.routes import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(title="Python Mongo Atlas", lifespan=lifespan, docs_url="/doc", redoc_url="/redoc")

register_error_handlers(app)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(items_router)


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI + MongoDB"}

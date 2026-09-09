from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from arq import create_pool

from app.api.services.auth.router import router as auth_router
from app.api.services.dashboard.router import router as dashboard_router
from app.config import settings
from app.worker.main import REDIS_SETTINGS


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_pool = await create_pool(REDIS_SETTINGS)
    app.state.redis = redis_pool
    yield
    await redis_pool.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret_key)

app.include_router(auth_router)
app.include_router(dashboard_router)

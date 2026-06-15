import os

from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine
from starlette.middleware.sessions import SessionMiddleware

from app.auth.router import router as auth_router

app = FastAPI()
app.include_router(auth_router)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

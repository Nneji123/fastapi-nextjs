from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import  add_pagination
from sqlalchemy.exc import IntegrityError

from api.config import Settings
from api.database import create_db_and_tables, create_town_and_people, get_db
from api.public.routes import public_router
from api.utils import *
from prometheus_fastapi_instrumentator import Instrumentator
import redis.asyncio as redis
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi_limiter import FastAPILimiter

env_path = "../.env"
load_dotenv(env_path)

REDIS_ENV = os.getenv("REDIS_DATABASE" ,"redis://redis:6379/")

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())  # Fetching the database session
    create_db_and_tables()
    redis_connection= redis.from_url(REDIS_ENV, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)
    try:
        create_town_and_people(db)
        yield
    except (IntegrityError, Exception) as e:
        yield


def create_app(settings: Settings):
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
        description=settings.DESCRIPTION,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://frontend:8080/",
        "http://frontend:8080/",
            "*"],
        # origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    app.include_router(public_router)
    Instrumentator().instrument(app).expose(app)
    add_pagination(app)
    return app

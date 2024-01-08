from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.exc import IntegrityError

from api.config import Settings
from api.database import create_db_and_tables, create_town_and_people, get_db
from api.public.routes import public_router
from api.utils import *

import redis.asyncio as redis
import uvicorn
from fastapi import Depends, FastAPI
from dotenv import load_dotenv
import os
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

env_path = "../.env"
load_dotenv(env_path)

REDIS_ENV = os.getenv("REDIS_DATABASE" ,"redis://default:Wls41vwKwXF5zuASsqoDG0mrwJHq82Pz@redis-14078.c325.us-east-1-4.ec2.cloud.redislabs.com:14078")

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
        # Perform any cleanup or teardown operations if needed
        yield

    # # Proceed with the rest of your code
    # async with self.lifespan_context(app) as maybe_state:
    #     # Other operations within the lifespan context
    #     pass


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
        allow_origins=["*"],
        # origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    app.include_router(public_router)

    return app

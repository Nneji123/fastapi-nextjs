from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

from api.config import Settings
from api.database import create_db_and_tables, create_town_and_people
from api.public.routes import public_router


from api.database import create_db_and_tables, create_town_and_people, get_db
from api.utils import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    async for db in get_db():  # Iterating over the asynchronous generator
        await create_db_and_tables()

        try:
            await create_town_and_people(db)
            yield
        except IntegrityError as e:
            # Perform any cleanup or teardown operations if needed
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
        allow_origins=["*"],
        # origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    app.include_router(public_router)

    return app

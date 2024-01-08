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
    db = next(get_db())  # Fetching the database session
    create_db_and_tables()

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

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from api.config import Settings
from api.database import create_db_and_tables, create_town_and_people
from api.public.towns.urls import town_router
from api.public.people.urls import people_router


from api.database import create_db_and_tables, create_town_and_people, get_db

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
    app.include_router(town_router)
    app.include_router(people_router)

    return app

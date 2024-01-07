from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import os
from sqlalchemy.exc import IntegrityError

from api.config import Settings
from api.database import create_db_and_tables, create_town_and_people
from api.public.towns.urls import town_router
from api.public.people.urls import people_router


from api.database import create_db_and_tables, create_town_and_people, get_db



lable_lang_mapping = {"Plain JS": "JavaScript", "NodeJS": "JavaScript"}

def add_examples(openapi_schema: dict, docs_dir):
    path_key = 'paths'
    code_key = 'x-codeSamples'

    for folder in os.listdir(docs_dir):
        base_path = os.path.join(docs_dir, folder)
        files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]
        for f in files:
            parts = f.split('-')
            if len(parts) >= 2:
                route = '/' + '/'.join(parts[:-1])
                method = parts[-1].split('.')[0]
                print(f'[{path_key}][{route}][{method}][{code_key}]')

                if route in openapi_schema[path_key]:
                    if code_key not in openapi_schema[path_key][route][method]:
                        openapi_schema[path_key][route][method].update({code_key: []})

                    openapi_schema[path_key][route][method][code_key].append({
                        'lang': lable_lang_mapping[folder],
                        'source': open(os.path.join(base_path, f), "r").read(),
                        'label': folder,
                    })
            else:
                print(f'Error in adding examples code to openapi {f}')

    return openapi_schema


def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = add_examples(openapi_schema, 'docs')

    return app.openapi_schema





origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


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
    app.openapi = custom_openapi(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(town_router)
    app.include_router(people_router)

    return app

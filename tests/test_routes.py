# test_routes.py

import pytest
from fastapi.testclient import TestClient
from api.app import app
from api.config import test_settings 
from api.database import create_db_and_tables, get_db
from api.public.towns.crud import create_town, get_town
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator


@pytest.fixture(scope="module")
async def db() -> AsyncGenerator:
    # Create an in-memory SQLite database
    async_engine = create_async_engine(test_settings.DATABASE_URI, echo=True)
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    database = Database(test_settings.DATABASE_URI)

    # Create the database tables
    await database.connect()
    await create_db_and_tables(async_engine)
    try:
        yield async_session
    finally:
        await database.disconnect()

@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_create_town(db: AsyncSession, client: TestClient):
    town_data = {"name": "TestTown", "population": 1000, "country": "TestCountry"}
    
    # Test creating a town
    response = client.post("/towns/", json=town_data)
    assert response.status_code == 200
    
    # Check if the town was created in the database
    created_town = await create_town(db, town_data)
    assert created_town.id is not None
    
    # Check if the created town matches the expected data
    fetched_town = await get_town(db, created_town.id)
    assert fetched_town.name == town_data["name"]
    assert fetched_town.population == town_data["population"]
    assert fetched_town.country == town_data["country"]

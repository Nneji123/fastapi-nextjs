from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.ext.asyncio import session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import sessionmaker
from api.public.people.crud import create_person
from api.public.towns.crud import create_town
from api.public.people.models import PersonCreate
from api.public.towns.models import TownCreate
from api.config import settings

connect_args = {"check_same_thread": False}
async_engine = create_async_engine(settings.DATABASE_URI)

# Create an asynchronous sessionmaker
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# def get_db():
#     with Session(engine) as session:
#         yield session




async def create_town_and_people(db: Session):
    # Create towns
    town_data = [
        {"name": "Town A", "population": 10000, "country": "Country A"},
        {"name": "Town B", "population": 15000, "country": "Country B"},
        # Add more towns as needed
    ]

    created_towns = []
    for town_info in town_data:
        town = TownCreate(**town_info)
        created_town = await create_town(db, town)
        created_towns.append(created_town)

    # Create people
    people_data = [
        {"name": "Alice", "age": 30, "town_id": created_towns[0].id},
        {"name": "Bob", "age": 25, "town_id": created_towns[1].id},
        # Assign people to towns created above, adjust town_id as needed
    ]

    created_people = []
    for person_info in people_data:
        person = PersonCreate(**person_info)
        created_person = await create_person(db, person)
        created_people.append(created_person)

    return created_towns, created_people

# async def connect_to_db():
#     await database.connect()

# async def close_db_connection():
#     await database.disconnect()

# def create_db_and_tables():
#     engine = create_engine(settings.DATABASE_URI, echo=True, connect_args={"check_same_thread": False})
#     SQLModel.metadata.create_all(engine)

# async def get_db() -> Session:
#     async with database.transaction():
#         yield Session()

# async def create_town_and_people(db: Session):
#     town_data = [
#         {"name": "Town A", "population": 10000, "country": "Country A"},
#         {"name": "Town B", "population": 15000, "country": "Country B"},
#         # Add more towns as needed
#     ]

#     created_towns = []
#     for town_info in town_data:
#         town = TownCreate(**town_info)
#         created_town = await create_town(db, town)
#         created_towns.append(created_town)

#     people_data = [
#         {"name": "Alice", "age": 30, "town_id": created_towns[0].id},
#         {"name": "Bob", "age": 25, "town_id": created_towns[1].id},
#         # Assign people to towns created above, adjust town_id as needed
#     ]

#     created_people = []
#     for person_info in people_data:
#         person = PersonCreate(**person_info)
#         created_person = await create_person(db, person)
#         created_people.append(created_person)

#     return created_towns, created_people

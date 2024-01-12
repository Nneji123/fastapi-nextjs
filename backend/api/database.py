from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.ext.asyncio import session

from api.config import settings
from api.public.people.crud import create_person
from api.public.people.models import PersonCreate
from api.public.towns.crud import create_town
from api.public.towns.models import TownCreate

# connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URI, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session


def create_town_and_people(db: Session):
    # Create towns
    town_data = [
        {"name": "Town A", "population": 10000, "country": "Country A"},
        {"name": "Town B", "population": 15000, "country": "Country B"},
        # Add more towns as needed
    ]

    created_towns = []
    for town_info in town_data:
        town = TownCreate(**town_info)
        created_town = create_town(db, town)
        created_towns.append(created_town)

    # Create people
    people_data = [
        {"name": "Alice", "age": 30, "gender": "female", "town_id": created_towns[0].id},
        {"name": "Bob", "age": 25, "gender": "male", "town_id": created_towns[1].id},
        # Assign people to towns created above, adjust town_id as needed
    ]

    created_people = []
    for person_info in people_data:
        person = PersonCreate(**person_info)
        created_person = create_person(db, person)
        created_people.append(created_person)

    return created_towns, created_people

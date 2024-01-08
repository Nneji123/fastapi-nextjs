from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.ext.asyncio import session

from api.database import create_db_and_tables, create_town_and_people, get_db


def create_database_for_tests():
    db = next(get_db())  # Fetching the database session
    create_db_and_tables()
    try:
        create_town_and_people(db)
    except (IntegrityError, Exception) as e:
        # Perform any cleanup or teardown operations if needed
        pass
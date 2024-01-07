from api.database import create_db_and_tables, create_town_and_people, get_db


if __name__=="__main__":
    db = next(get_db())  # Fetching the database session
    create_db_and_tables()

    create_town_and_people(db)

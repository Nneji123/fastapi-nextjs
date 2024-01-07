from typing import Optional, List
from sqlmodel import Session, select
from api.public.towns.models import Town, TownCreate, TownUpdate


async def create_town(db: Session, town: TownCreate) -> Town:
    """
    The create_town function creates a new town in the database.

    :param db: Session: Pass a database session to the function
    :param town: TownCreate: Create a new town object
    :return: The town object that was created
    """
    db_town = Town(**town.model_dump())
    db.add(db_town)
    await db.commit()
    await db.refresh(db_town)
    return db_town


async def get_town(db: Session, town_id: int) -> Optional[Town]:
    """
    The get_town function returns a town object from the database.

    :param db: Session: Pass the database session into the function
    :param town_id: int: Filter the town by id
    :return: An object of the town class
    """
    query = select(Town).where(Town.id == town_id)
    return await db.exec(query).first()

async def get_towns(db: Session, skip: int = 0, limit: int = 10) -> List[Town]:
    """
    The get_towns function returns a list of towns from the database.

    :param db: Session: Pass the database session to the function
    :param skip: int: Skip a number of rows in the database
    :param limit: int: Limit the number of results returned
    :return: A list of town objects
    """
    query = select(Town).offset(skip).limit(limit)
    return await db.exec(query).all()


async def update_town(db: Session, town: Town, updated_town: TownUpdate) -> Town:
    """
    The update_town function updates a town in the database.

    :param db: Session: Pass in the database session
    :param town: Town: Get the town that is being updated
    :param updated_town: TownUpdate: Pass in the updated values of the town
    :return: The updated town
    """
    for key, value in updated_town.model_dump(exclude_unset=True).items():
        setattr(town, key, value)
    db.add(town)
    await db.commit()
    await db.refresh(town)
    return town


async def delete_town(db: Session, town_id: int) -> Town:
    """
    The delete_town function deletes a town from the database.

    :param db: Session: Connect to the database
    :param town_id: int: Specify which town to delete
    :return: The deleted town
    """
    town = db.exec(select(Town).where(Town.id == town_id)).first()
    db.delete(town)
    await db.commit()
    return town

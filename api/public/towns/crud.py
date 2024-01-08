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
    town = (await db.execute(select(Town.id, Town.name, Town.population, Town.country).where(Town.id == town_id))).first()
    return town


async def get_towns(db: Session, skip: int = 0, limit: int = 10) -> List[Town]:
    query = select(Town).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def delete_town(db: Session, town_id: int):
    town = await db.execute(select(Town).where(Town.id == town_id))
    town_to_delete = town.scalar_one_or_none()

    if town_to_delete:
        await db.delete(town_to_delete)
        await db.commit()

    return town_to_delete

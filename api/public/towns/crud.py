from typing import List, Optional

from sqlmodel import Session, select

from api.public.towns.models import Town, TownCreate, TownUpdate


def create_town(db: Session, town: TownCreate) -> Town:
    db_town = Town(**town.model_dump())
    db.add(db_town)
    db.commit()
    db.refresh(db_town)
    return db_town


def get_town(db: Session, town_id: int) -> Optional[Town]:
    query = select(Town).where(Town.id == town_id)
    return db.exec(query).first()


def get_towns(db: Session, skip: int = 0, limit: int = 10) -> List[Town]:
    query = select(Town).offset(skip).limit(limit)
    return db.exec(query).all()


def update_town(db: Session, town: Town, updated_town: TownUpdate) -> Town:
    for key, value in updated_town.model_dump(exclude_unset=True).items():
        setattr(town, key, value)
    db.add(town)
    db.commit()
    db.refresh(town)
    return town


def delete_town(db: Session, town_id: int) -> Town:
    town = db.get(Town, town_id)
    if town:
        db.delete(town)
        db.commit()
    return town

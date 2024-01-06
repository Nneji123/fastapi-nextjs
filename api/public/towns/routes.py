from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api.public.towns.crud import create_town, get_town, get_towns, update_town, delete_town
from api.public.towns.models import TownCreate, TownRead, TownUpdate

router = APIRouter(prefix="/towns", tags=["Towns"])


@router.post("/", response_model=TownRead)
def create_new_town(town: TownCreate, db: Session = Depends(get_db)):
    return create_town(db, town)


@router.get("/{town_id}", response_model=TownRead)
def get_single_town(town_id: int, db: Session = Depends(get_db)):
    town = get_town(db, town_id)
    if town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return town


@router.get("/", response_model=List[TownRead])
def get_all_towns(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_towns(db, skip=skip, limit=limit)


@router.put("/{town_id}", response_model=TownRead)
def update_existing_town(town_id: int, town: TownUpdate, db: Session = Depends(get_db)):
    """
    The update_existing_town function updates an existing town in the database.

    :param town_id: int: Identify the town to be updated
    :param town: TownUpdate: Pass in the new data for the town
    :param db: Session: Pass the database session to the function
    :return: The updated town object
    """
    existing_town = get_town(db, town_id)
    if existing_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return update_town(db, existing_town, town)


@router.delete("/{town_id}", response_model=TownRead)
def delete_existing_town(town_id: int, db: Session = Depends(get_db)):
    """
    The delete_existing_town function deletes a town from the database.
        It takes in an integer, town_id, and returns a boolean value indicating whether or not the deletion was successful.

    :param town_id: int: Specify the id of the town to be deleted
    :param db: Session: Pass in the database session
    :return: The result of delete_town
    """
    town = get_town(db, town_id)
    if town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return delete_town(db, town_id)

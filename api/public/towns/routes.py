from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api.public.towns.crud import create_town, get_town, get_towns, update_town, delete_town
from api.public.towns.models import TownCreate, TownRead, TownUpdate, TownReadWithPeople

router = APIRouter()


@router.post("/", openapi_extra={"x-codeSamples": [{"lang": "Python", "source": "print('FastAPI!')", "label": "Python"}]}, response_model=TownRead)
async def create_new_town(town: TownCreate, db: Session = Depends(get_db)):
    try:
        created_town = await create_town(db, town)
        return JSONResponse(content={"status": "success", "msg": "Town created successfully", "data": created_town.dict()})
    except Exception as e:
        return JSONResponse(content={"status": "error", "msg": f"Failed to create town: {str(e)}"}, status_code=500)


@router.get("/{town_id}", response_model=TownRead) # Change townreadwithpeople
async def get_single_town(town_id: int, db: Session = Depends(get_db)):
    town = await get_town(db, town_id)
    if town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return town


@router.get("/", response_model=List[TownRead])
async def get_all_towns(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return await get_towns(db, skip=skip, limit=limit)


@router.put("/{town_id}", response_model=TownRead)
async def update_existing_town(town_id: int, town: TownUpdate, db: Session = Depends(get_db)):
    """
    The update_existing_town function updates an existing town in the database.

    :param town_id: int: Identify the town to be updated
    :param town: TownUpdate: Pass in the new data for the town
    :param db: Session: Pass the database session to the function
    :return: The updated town object
    """
    existing_town = await get_town(db, town_id)
    if existing_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return await update_town(db, existing_town, town)


@router.delete("/{town_id}", response_model=TownRead)
async def delete_existing_town(town_id: int, db: Session = Depends(get_db)):
    """
    The delete_existing_town function deletes a town from the database.
        It takes in an integer, town_id, and returns a boolean value indicating whether or not the deletion was successful.

    :param town_id: int: Specify the id of the town to be deleted
    :param db: Session: Pass in the database session
    :return: The result of delete_town
    """

    delete_result = await delete_town(db, town_id)
    if delete_result:
        return JSONResponse(content={"status": "success", "msg": f"Successfully deleted town with ID {town_id}"})
    else:
        return JSONResponse(content={"status": "error", "msg": f"Failed to delete town with ID {town_id}"}, status_code=500)

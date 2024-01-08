from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api.public.towns.crud import create_town, get_town, get_towns, delete_town, update_town
from api.public.towns.models import TownCreate, TownRead, TownUpdate, TownReadWithPeople, Town

router = APIRouter()


@router.post("/", response_model=TownRead)
def create_new_town(town: TownCreate, db: Session = Depends(get_db)):
    try:
        created_town = create_town(db, town)
        return JSONResponse(content={"status": "success", "msg": "Town created successfully", "data": created_town.dict()})
    except Exception as e:
        return JSONResponse(content={"status": "error", "msg": f"Failed to create town: {str(e)}"}, status_code=500)


@router.get("/{town_id}", response_model=TownReadWithPeople)
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
    existing_town = get_town(db, town_id)
    if existing_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return update_town(db, existing_town, town)


@router.delete("/{town_id}", response_model=TownRead)
def delete_existing_town(town_id: int, db: Session = Depends(get_db)):
    delete_result = delete_town(db, town_id)
    if delete_result:
        return JSONResponse(content={"status": "success", "msg": f"Successfully deleted town with ID {town_id}"})
    else:
        return JSONResponse(content={"status": "error", "msg": f"Failed to delete town with ID {town_id}"}, status_code=500)
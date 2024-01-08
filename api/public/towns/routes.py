from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api.public.towns.crud import create_town, get_town, get_towns, delete_town
from api.public.towns.models import TownCreate, TownRead, TownUpdate, TownReadWithPeople, Town

router = APIRouter()


@router.post("/", openapi_extra={"x-codeSamples": [{"lang": "Python", "source": "print('FastAPI!')", "label": "Python"}]}, response_model=TownRead)
async def create_new_town(town: TownCreate, db: Session = Depends(get_db)):
    try:
        created_town = await create_town(db, town)
        return JSONResponse(content={"status": "success", "msg": "Town created successfully", "data": created_town.dict()})
    except Exception as e:
        return JSONResponse(content={"status": "error", "msg": f"Failed to create town: {str(e)}"}, status_code=500)


@router.get("/{town_id}", response_model=TownReadWithPeople) # Change townreadwithpeople
async def get_single_town(town_id: int, db: Session = Depends(get_db)):
    town = await get_town(db, town_id)
    if town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return town


@router.get("/", response_model=List[TownRead])
async def get_all_towns(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return await get_towns(db, skip=skip, limit=limit)


@router.put("/{town_id}", response_model=TownRead)
async def update_existing_town(town_id: int, town_update: TownUpdate, db: Session = Depends(get_db)):
    existing_town = await db.get(Town, town_id)
    if not existing_town:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Town not found with id: {town_id}",
        )

    updated_values = town_update.model_dump(exclude_unset=True)
    for key, value in updated_values.items():
        setattr(existing_town, key, value)

    db.add(existing_town)
    await db.commit()
    await db.refresh(existing_town)
    return existing_town


@router.delete("/{town_id}", response_model=TownRead)
async def delete_existing_town(town_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing town
    """

    delete_result = await delete_town(db, town_id)
    if delete_result:
        return JSONResponse(content={"status": "success", "msg": f"Successfully deleted town with ID {town_id}"})
    else:
        return JSONResponse(content={"status": "error", "msg": f"Failed to delete town with ID {town_id}"}, status_code=500)

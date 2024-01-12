from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from api.database import get_db
from api.public.towns.crud import (
    create_town,
    delete_town,
    get_town,
    get_towns,
    update_town,
)
from api.public.towns.models import (
    Town,
    TownCreate,
    TownRead,
    TownReadWithPeople,
    TownUpdate,
)

router = APIRouter()
disable_installed_extensions_check()

@router.post("/", response_model=TownRead)
def create_new_town(town: TownCreate, db: Session = Depends(get_db)):
    try:
        created_town = create_town(db, town)
        return JSONResponse(
            content={
                "status": "success",
                "msg": "Town created successfully",
                "data": created_town.model_dump(),
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "msg": f"Failed to create town: {str(e)}"},
            status_code=500,
        )


@router.get("/{town_id}", response_model=TownReadWithPeople)
def get_single_town(town_id: int, db: Session = Depends(get_db)):
    town = get_town(db, town_id)
    if town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return town


@router.get("/", response_model=Page[TownRead])
def get_all_towns(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return paginate(get_towns(db, skip=skip, limit=limit))


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
        return JSONResponse(
            content={
                "status": "success",
                "msg": f"Successfully deleted town with ID {town_id}",
            }
        )
    else:
        return JSONResponse(
            content={
                "status": "error",
                "msg": f"Failed to delete town with ID {town_id}",
            },
            status_code=500,
        )

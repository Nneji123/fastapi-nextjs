from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse
from sqlmodel import Session
from api.public.people.crud import get_person, get_people, update_person, delete_person, create_person
from api.public.people.models import PersonUpdate, PersonCreate, Person, PersonRead, PersonReadWithTown
from api.database import get_db

router = APIRouter()

@router.get("/{person_id}", response_model=PersonReadWithTown)
async def get_single_person(person_id: int, db: Session = Depends(get_db)):
    person = await get_person(db, person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.get("/", response_model=list[PersonRead])
async def get_all_people(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return await get_people(db, skip=skip, limit=limit)

@router.post("/", response_model=Person)
async def create_new_person(person: PersonCreate, db: Session = Depends(get_db)):
    try:
        created_person = await create_person(db, person)
        return created_person
    except Exception as e:
        return JSONResponse(content={"status": "error", "msg": f"Failed to create person: {str(e)}"}, status_code=500)

@router.put("/{person_id}", response_model=Person)
async def update_existing_person(person_id: int, updated_person: PersonUpdate, db: Session = Depends(get_db)):
    person = await get_person(db, person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    try:
        updated = update_person(db, person, updated_person)
        return updated
    except Exception as e:
        return JSONResponse(content={"status": "error", "msg": f"Failed to update person: {str(e)}"}, status_code=500)

@router.delete("/{person_id}", response_model=Person)
async def delete_existing_person(person_id: int, db: Session = Depends(get_db)):
    person = await get_person(db, person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    try:
        deleted = await delete_person(db, person_id)
        return deleted
    except Exception as e:
        return JSONResponse(content={"status": "error", "msg": f"Failed to delete person: {str(e)}"}, status_code=500)

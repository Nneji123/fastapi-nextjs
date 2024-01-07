from typing import Optional, List
from sqlmodel import Session, select
from api.public.people.models import Person, PersonCreate, PersonUpdate


async def create_person(db: Session, person: PersonCreate) -> Person:
    db_person = Person(**person.model_dump())
    db.add(db_person)
    await db.commit()
    await db.refresh(db_person)
    return db_person


async def get_person(db: Session, person_id: int) -> Optional[Person]:
    query = select(Person).where(Person.id == person_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_people(db: Session, skip: int = 0, limit: int = 10) -> List[Person]:
    query = select(Person).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def update_person(db: Session, person: Person, updated_person: PersonUpdate) -> Person:
    for key, value in updated_person.model_dump(exclude_unset=True).items():
        setattr(person, key, value)
    db.add(person)
    await db.commit()
    await db.refresh(person)
    return person


async def delete_person(db: Session, person_id: int) -> Person:
    person = await db.execute(select(Person).where(Person.id == person_id))
    db.delete(person.scalar_one())
    await db.commit()
    return person.scalar_one()

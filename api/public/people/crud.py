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
    person = (await db.execute(select(Person.id, Person.name, Person.gender, Person.age, Person.town_id).where(Person.id == person_id))).first()
    return person


async def get_people(db: Session, skip: int = 0, limit: int = 10) -> List[Person]:
    query = select(Person).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def delete_person(db: Session, person_id: int) -> Person:
    person = await db.execute(select(Person).where(Person.id == person_id))
    person_to_delete = person.scalar_one_or_none()

    if person_to_delete:
        await db.delete(person_to_delete)
        await db.commit()

    return person_to_delete

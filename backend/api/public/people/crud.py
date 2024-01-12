from typing import List, Optional

from sqlmodel import Session, select

from api.public.people.models import Person, PersonCreate, PersonUpdate


def create_person(db: Session, person: PersonCreate) -> Person:
    db_person = Person(**person.model_dump())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def get_person(db: Session, person_id: int) -> Optional[Person]:
    query = select(Person).where(Person.id == person_id)
    return db.exec(query).first()


def get_people(db: Session, skip: int = 0, limit: int = 10) -> List[Person]:
    query = select(Person).offset(skip).limit(limit)
    return db.exec(query).all()


def update_person(db: Session, person: Person, updated_person: PersonUpdate) -> Person:
    for key, value in updated_person.model_dump(exclude_unset=True).items():
        setattr(person, key, value)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def delete_person(db: Session, person_id: int) -> Person:
    person = db.get(Person, person_id)
    db.delete(person)
    db.commit()
    return person

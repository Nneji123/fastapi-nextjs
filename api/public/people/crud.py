from typing import Optional, List
from sqlmodel import Session, select
from api.public.people.models import Person, PersonCreate, PersonUpdate


def create_person(db: Session, person: PersonCreate) -> Person:
    db_person = Person(**person.model_dump())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def get_person(db: Session, person_id: int) -> Optional[Person]:
    return db.exec(Person).filter(Person.id == person_id).first()


def get_people(db: Session, skip: int = 0, limit: int = 10) -> List[Person]:
    return db.exec(Person).offset(skip).limit(limit).all()


def update_person(db: Session, person: Person, updated_person: PersonUpdate) -> Person:
    for key, value in updated_person.model_dump(exclude_unset=True).items():
        setattr(person, key, value)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def delete_person(db: Session, person_id: int) -> Person:
    person = db.exec(Person).filter(Person.id == person_id).first()
    db.delete(person)
    db.commit()
    return person

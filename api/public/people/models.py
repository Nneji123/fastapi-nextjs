from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.public.towns.models import Town


class PersonBase(SQLModel):
    name: str = Field(index=True, unique=True)
    gender: Optional[str] = Field(index=True)
    age: Optional[int] = Field(default=None, index=True)
    town_id: Optional[int] = Field(default=None, foreign_key="town.id")


class Person(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    towns: Optional["Town"] = Relationship(back_populates="people")


class PersonCreate(PersonBase):
    pass


class PersonRead(PersonBase):
    id: int


class PersonUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    town_id: Optional[int] = None


class PersonReadWithTown(PersonRead):
    town: Optional[PersonRead] = None

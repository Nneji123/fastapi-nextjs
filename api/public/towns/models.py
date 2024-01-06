from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from api.public.people.models import Person


class TownBase(SQLModel):
    """Base Town class"""
    name: str = Field(index=True)
    population: int = Field(default=None, index=True)
    country: Optional[str] = Field(default=None)

class Town(TownBase, table=True):
    """Town Table"""
    id: Optional[int] = Field(default=None, primary_key=True)

    people: List["Person"] = Relationship(back_populates="towns")


class TownCreate(TownBase):
    """Create a town"""
    pass

class TownRead(TownBase):
    """Read details of a town."""
    id: int

class TownUpdate(SQLModel):
    """Update details of a town."""
    name: Optional[str] = None
    population: Optional[int] = None
    country: Optional[str] = None


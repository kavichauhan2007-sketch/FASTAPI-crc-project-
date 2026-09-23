from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel

class StatusEnum(str, Enum):
    Lost = "Lost"
    Found = "Found"
    Returned = "Returned"

class ItemBase(SQLModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=5)
    category: str
    location: str
    reported_by: str
    status: StatusEnum

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=5)
    category: Optional[str] = None
    location: Optional[str] = None
    reported_by: Optional[str] = None
    status: Optional[StatusEnum] = None

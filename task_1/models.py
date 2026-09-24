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
    id: int | None = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=5)
    category: str | None = None
    location: str | None = None
    reported_by: str | None = None
    status: StatusEnum | None = None

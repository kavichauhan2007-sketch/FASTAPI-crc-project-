from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class EventStatus(str, Enum):
    Open = "Open"
    Closed = "Closed"


class EventBase(SQLModel):
    title: str = Field(min_length=1)
    venue: str = Field(min_length=1)
    capacity: int = Field(gt=0)
    organizer: str = Field(min_length=1)
    status: EventStatus = Field(default=EventStatus.Open)


class Event(EventBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class EventCreate(EventBase):
    pass


class EventUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1)
    venue: str | None = Field(default=None, min_length=1)
    capacity: int | None = Field(default=None, gt=0)
    organizer: str | None = Field(default=None, min_length=1)
    status: EventStatus | None = None


class ReservationBase(SQLModel):
    student_name: str = Field(min_length=1)
    roll_number: str = Field(min_length=1)
    email: EmailStr


class Reservation(ReservationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")


class ReservationCreate(ReservationBase):
    pass


class AvailabilityResponse(SQLModel):
    capacity: int
    booked: int
    remaining: int

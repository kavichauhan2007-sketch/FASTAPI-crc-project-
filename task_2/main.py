from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel, select

from .database import engine, get_session
from .models import (
    AvailabilityResponse,
    Event,
    EventCreate,
    EventStatus,
    EventUpdate,
    Reservation,
    ReservationCreate,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(title="Event Reservation API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/events", response_model=Event, status_code=201)
def create_event(event: EventCreate, db: SessionDep):
    db_event = Event.model_validate(event)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@app.get("/events", response_model=list[Event])
def read_events(db: SessionDep):
    events = db.exec(select(Event)).all()
    return events


@app.get("/events/{event_id}", response_model=Event)
def read_event(event_id: int, db: SessionDep):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.put("/events/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventUpdate, db: SessionDep):
    db_event = db.get(Event, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event_data = event.model_dump(exclude_unset=True)
    for key, value in event_data.items():
        setattr(db_event, key, value)
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: SessionDep):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Delete associated reservations
    reservations = db.exec(select(Reservation).where(Reservation.event_id == event_id)).all()
    for res in reservations:
        db.delete(res)
        
    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}


@app.post("/events/{event_id}/reserve", response_model=Reservation, status_code=201)
def create_reservation(event_id: int, reservation: ReservationCreate, db: SessionDep):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event.status != EventStatus.Open:
        raise HTTPException(status_code=400, detail="Event is closed for reservations")
    
    existing_reservations = db.exec(select(Reservation).where(Reservation.event_id == event_id)).all()
    booked = len(existing_reservations)
    
    if booked >= event.capacity:
        raise HTTPException(status_code=400, detail="Event is already full")
        
    db_reservation = Reservation.model_validate(reservation)
    db_reservation.event_id = event_id
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


@app.get("/events/{event_id}/reservations", response_model=list[Reservation])
def read_event_reservations(event_id: int, db: SessionDep):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    reservations = db.exec(select(Reservation).where(Reservation.event_id == event_id)).all()
    return reservations


@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, db: SessionDep):
    reservation = db.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(reservation)
    db.commit()
    return {"message": "Reservation cancelled successfully"}


@app.get("/events/{event_id}/availability", response_model=AvailabilityResponse)
def read_event_availability(event_id: int, db: SessionDep):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    reservations = db.exec(select(Reservation).where(Reservation.event_id == event_id)).all()
    booked = len(reservations)
    remaining = event.capacity - booked
    
    return AvailabilityResponse(
        capacity=event.capacity,
        booked=booked,
        remaining=remaining
    )

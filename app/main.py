from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from .database import get_db, engine, Base
from .models import models
from .schemas import schemas
from .services import flight_service
from .scripts.seed_data import seed_data

# Create tables
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flight_booking")

app = FastAPI(title="Flight Booking API")

@app.get("/flights", response_model=list[schemas.Flight])
def list_flights(db: Session = Depends(get_db)):
    """List all available flights"""
    return flight_service.list_flights(db)

@app.get("/flights/search", response_model=list[schemas.Flight])
def search_flights(
    origin: str | None = None,
    destination: str | None = None,
    departure_date: datetime | None = None,
    flight_class: str | None = None,
    adults: int | None = None,
    db: Session = Depends(get_db)
):
    """
    Search for flights with optional filters.
    All parameters are optional - if none are provided, returns all flights.
    """
    flights = flight_service.search_flights(
        db=db,
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        flight_class=flight_class,
        adults=adults
    )
    return flights

@app.get("/flights/{flight_id}", response_model=schemas.Flight)
def get_flight(flight_id: str, db: Session = Depends(get_db)):
    flight = flight_service.get_flight(db, flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight

@app.get("/bookings", response_model=list[schemas.Booking])
def list_bookings(db: Session = Depends(get_db)):
    """List all bookings"""
    return flight_service.list_bookings(db)

@app.post("/bookings", response_model=schemas.Booking, status_code=status.HTTP_201_CREATED)
def create_booking(booking_request: schemas.BookingRequest, db: Session = Depends(get_db)):
    booking = flight_service.create_booking(
        db=db,
        flight_id=booking_request.flight_id,
        passengers=booking_request.passengers,
        contact_email=booking_request.contact_email,
        contact_phone=booking_request.contact_phone
    )
    if not booking:
        raise HTTPException(status_code=400, detail="Could not create booking")
    return booking

@app.get("/bookings/{booking_id}", response_model=schemas.Booking)
def get_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = flight_service.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.delete("/bookings/{booking_id}", response_model=schemas.Booking)
def cancel_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = flight_service.cancel_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.get("/passengers", response_model=list[schemas.PassengerInfo])
def list_passengers(db: Session = Depends(get_db)):
    """List all passengers"""
    return flight_service.list_passengers(db)

@app.on_event("startup")
async def startup_event():
    seed_data()

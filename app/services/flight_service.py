from datetime import datetime, time, timedelta
from sqlalchemy.orm import Session
from app.models.models import FlightModel, BookingModel, PassengerModel
import uuid

def search_flights(
    db: Session,
    origin: str | None = None,
    destination: str | None = None,
    departure_date: datetime | None = None,
    flight_class: str | None = None,
    adults: int | None = None
):
    query = db.query(FlightModel)

    if origin:
        query = query.filter(FlightModel.origin_airport_code == origin)
    if destination:
        query = query.filter(FlightModel.destination_airport_code == destination)
    if flight_class:
        query = query.filter(FlightModel.flight_class == flight_class)
    if adults:
        query = query.filter(FlightModel.available_seats >= adults)

    if departure_date:
        next_date = departure_date + timedelta(days=1)
        query = query.filter(
            FlightModel.departure_time >= datetime.combine(departure_date, time.min),
            FlightModel.departure_time < datetime.combine(next_date, time.min)
        )

    return query.all()

def get_flight(db: Session, flight_id: str):
    return db.query(FlightModel).filter(FlightModel.flight_id == flight_id).first()

def create_booking(db: Session, flight_id: str, passengers: list, contact_email: str, contact_phone: str):
    flight = get_flight(db, flight_id)
    if not flight or flight.available_seats < len(passengers):
        return None

    booking_id = str(uuid.uuid4())
    booking = BookingModel(
        booking_id=booking_id,
        flight_id=flight_id,
        booking_status="CONFIRMED",
        total_price=flight.price * len(passengers),
        booking_date=datetime.now(),
        contact_email=contact_email,
        contact_phone=contact_phone
    )
    db.add(booking)

    for passenger in passengers:
        db.add(PassengerModel(
            booking_id=booking_id,
            first_name=passenger.first_name,
            last_name=passenger.last_name,
            passport_number=passenger.passport_number
        ))

    flight.available_seats -= len(passengers)
    db.commit()
    return db.query(BookingModel).filter(BookingModel.booking_id == booking_id).first()

def cancel_booking(db: Session, booking_id: str):
    booking = db.query(BookingModel).filter(BookingModel.booking_id == booking_id).first()
    if not booking:
        return None

    booking.booking_status = "CANCELLED"
    flight = get_flight(db, booking.flight_id)
    flight.available_seats += len(booking.passengers)
    db.commit()
    return booking

def get_booking(db: Session, booking_id: str):
    return db.query(BookingModel).filter(BookingModel.booking_id == booking_id).first()

def list_flights(db: Session):
    return db.query(FlightModel).all()

def list_bookings(db: Session):
    return db.query(BookingModel).all()

def list_passengers(db: Session):
    return db.query(PassengerModel).all()

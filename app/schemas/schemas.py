from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from app.models.models import FlightClassEnum

class FlightSearch(BaseModel):
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    departure_date: date
    adults: int = Field(1, ge=1)
    flight_class: FlightClassEnum = FlightClassEnum.ECONOMY

class Flight(BaseModel):
    flight_id: str
    airline: str
    flight_number: str
    origin_airport_code: str
    destination_airport_code: str
    departure_time: datetime
    arrival_time: datetime
    available_seats: int
    price: float
    flight_class: FlightClassEnum

    class Config:
        from_attributes = True

class PassengerInfo(BaseModel):
    first_name: str
    last_name: str
    passport_number: Optional[str] = None

    class Config:
        from_attributes = True

class BookingRequest(BaseModel):
    flight_id: str
    passengers: List[PassengerInfo]
    contact_email: str
    contact_phone: str

class Booking(BaseModel):
    booking_id: str
    flight_id: str
    booking_status: str
    passengers: List[PassengerInfo]
    total_price: float
    booking_date: datetime
    contact_email: str
    contact_phone: str

    class Config:
        from_attributes = True

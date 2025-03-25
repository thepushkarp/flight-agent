from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class FlightClassEnum(str, enum.Enum):
    ECONOMY = "economy"
    BUSINESS = "business"
    FIRST = "first"

class FlightModel(Base):
    __tablename__ = "flights"
    flight_id = Column(String, primary_key=True, index=True)
    airline = Column(String, nullable=False)
    flight_number = Column(String, nullable=False)
    origin_airport_code = Column(String(3), nullable=False)
    destination_airport_code = Column(String(3), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    available_seats = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    flight_class = Column(Enum(FlightClassEnum), nullable=False)
    bookings = relationship("BookingModel", back_populates="flight")

class BookingModel(Base):
    __tablename__ = "bookings"
    booking_id = Column(String, primary_key=True, index=True)
    flight_id = Column(String, ForeignKey("flights.flight_id"), nullable=False)
    booking_status = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
    booking_date = Column(DateTime, nullable=False)
    contact_email = Column(String, nullable=False)
    contact_phone = Column(String, nullable=False)
    flight = relationship("FlightModel", back_populates="bookings")
    passengers = relationship("PassengerModel", back_populates="booking")

class PassengerModel(Base):
    __tablename__ = "passengers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(String, ForeignKey("bookings.booking_id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    passport_number = Column(String, nullable=True)
    booking = relationship("BookingModel", back_populates="passengers")

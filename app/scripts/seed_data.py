from datetime import datetime, timedelta
import uuid
from ..database import SessionLocal
from ..models.models import FlightModel, BookingModel, PassengerModel, FlightClassEnum

def create_flight(db, flight_data):
    flight = FlightModel(**flight_data)
    db.add(flight)
    return flight

def create_booking_with_passengers(db, flight, passengers_data, contact_data):
    booking_id = str(uuid.uuid4())
    booking = BookingModel(
        booking_id=booking_id,
        flight_id=flight.flight_id,
        booking_status="CONFIRMED",
        total_price=flight.price * len(passengers_data),
        booking_date=datetime.now(),
        **contact_data
    )
    db.add(booking)

    for passenger_data in passengers_data:
        passenger = PassengerModel(
            booking_id=booking_id,
            **passenger_data
        )
        db.add(passenger)

    flight.available_seats -= len(passengers_data)
    return booking

def seed_data():
    db = SessionLocal()

    # Clear existing data
    db.query(PassengerModel).delete()
    db.query(BookingModel).delete()
    db.query(FlightModel).delete()

    # Define base date for flights
    base_date = datetime.now() + timedelta(days=7)

    # Domestic Routes
    domestic_routes = [
        ("DEL", "BOM", "Delhi", "Mumbai", "Air India", "AI", 2.5, 5500),
        ("BOM", "DEL", "Mumbai", "Delhi", "Air India", "AI", 2.5, 5800),
        ("DEL", "BLR", "Delhi", "Bangalore", "IndiGo", "6E", 3, 6500),
        ("BLR", "DEL", "Bangalore", "Delhi", "IndiGo", "6E", 3, 6800),
        ("BOM", "CCU", "Mumbai", "Kolkata", "Vistara", "UK", 3, 7000),
        ("BLR", "HYD", "Bangalore", "Hyderabad", "SpiceJet", "SG", 1.5, 3500),
        ("DEL", "MAA", "Delhi", "Chennai", "Air India", "AI", 3, 6000),
        ("CCU", "BLR", "Kolkata", "Bangalore", "IndiGo", "6E", 3, 6200),
    ]

    # International Routes
    international_routes = [
        ("DEL", "DXB", "Delhi", "Dubai", "Emirates", "EK", 4, 25000),
        ("BOM", "SIN", "Mumbai", "Singapore", "Singapore Airlines", "SQ", 6, 35000),
        ("DEL", "LHR", "Delhi", "London", "British Airways", "BA", 9, 55000),
        ("BLR", "SFO", "Bangalore", "San Francisco", "United", "UA", 17, 85000),
        ("DEL", "JFK", "Delhi", "New York", "Air India", "AI", 16, 75000),
        ("BOM", "HKG", "Mumbai", "Hong Kong", "Cathay Pacific", "CX", 6, 40000),
    ]

    # Create flights for next 30 days
    all_flights = []
    for days in range(30):
        current_date = base_date + timedelta(days=days)

        # Create domestic flights
        for route in domestic_routes:
            origin, dest, origin_city, dest_city, airline, code, duration, price = route
            flight_id = f"{code}{str(uuid.uuid4())[:6]}"

            # Morning flight
            departure_time = current_date.replace(hour=6, minute=0)
            all_flights.append(create_flight(db, {
                "flight_id": f"M{flight_id}",
                "airline": airline,
                "flight_number": f"{code}{100+days}M",
                "origin_airport_code": origin,
                "destination_airport_code": dest,
                "departure_time": departure_time,
                "arrival_time": departure_time + timedelta(hours=duration),
                "available_seats": 180,
                "price": price,
                "flight_class": FlightClassEnum.ECONOMY
            }))

            # Evening flight
            departure_time = current_date.replace(hour=18, minute=0)
            all_flights.append(create_flight(db, {
                "flight_id": f"E{flight_id}",
                "airline": airline,
                "flight_number": f"{code}{100+days}E",
                "origin_airport_code": origin,
                "destination_airport_code": dest,
                "departure_time": departure_time,
                "arrival_time": departure_time + timedelta(hours=duration),
                "available_seats": 180,
                "price": price * 1.2,  # Evening flights slightly more expensive
                "flight_class": FlightClassEnum.ECONOMY
            }))

        # Create international flights (one per day)
        for route in international_routes:
            origin, dest, origin_city, dest_city, airline, code, duration, price = route
            flight_id = f"{code}{str(uuid.uuid4())[:6]}"
            departure_time = current_date.replace(hour=10, minute=0)

            all_flights.append(create_flight(db, {
                "flight_id": flight_id,
                "airline": airline,
                "flight_number": f"{code}{200+days}",
                "origin_airport_code": origin,
                "destination_airport_code": dest,
                "departure_time": departure_time,
                "arrival_time": departure_time + timedelta(hours=duration),
                "available_seats": 300,
                "price": price,
                "flight_class": FlightClassEnum.ECONOMY
            }))

    # Create some sample bookings and passengers
    sample_passengers = [
        {"first_name": "Rahul", "last_name": "Kumar", "passport_number": "A1234567"},
        {"first_name": "Priya", "last_name": "Singh", "passport_number": "B2345678"},
        {"first_name": "Amit", "last_name": "Patel", "passport_number": "C3456789"},
        {"first_name": "Sneha", "last_name": "Sharma", "passport_number": "D4567890"},
        {"first_name": "Raj", "last_name": "Malhotra", "passport_number": "E5678901"},
    ]

    contact_details = [
        {"contact_email": "rahul@example.com", "contact_phone": "+91-9876543210"},
        {"contact_email": "priya@example.com", "contact_phone": "+91-9876543211"},
        {"contact_email": "amit@example.com", "contact_phone": "+91-9876543212"},
    ]

    # Create bookings for some flights
    for i, flight in enumerate(all_flights[:10]):  # Create bookings for first 10 flights
        passengers = sample_passengers[i % 2:i % 2 + 2]  # Take 2 passengers at a time
        contact = contact_details[i % len(contact_details)]
        create_booking_with_passengers(db, flight, passengers, contact)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()

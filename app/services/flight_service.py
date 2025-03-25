from datetime import datetime
from typing import List, Optional, Dict, Any
from app.services.amadeus_service import (
    search_flights as search_flights_amadeus,
    create_flight_booking as create_amadeus_booking,
    get_booking_details,
    cancel_booking as cancel_amadeus_booking,
    search_airports_cities,
    get_flight_destinations as get_flight_destinations_amadeus,
    get_flight_offer_price as get_flight_offer_price_amadeus
)

def search_locations(keyword: str, location_type: Optional[str] = None) -> List[dict]:
    """
    Search for airports and cities
    """
    return search_airports_cities(keyword, location_type)

def get_flight_destinations(origin: str) -> List[dict]:
    """
    Get direct flight destinations from an origin
    """
    return get_flight_destinations_amadeus(origin)

def search_flights(
    origin: str,
    destination: str,
    departure_date: datetime,
    adults: int
) -> List[dict]:
    """
    Search for flights using the Amadeus API.
    """
    return search_flights_amadeus(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        adults=adults
    )

def get_flight_offer_price(
    flight_offer: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Get the price of a flight offer
    """
    return get_flight_offer_price_amadeus(flight_offer)

def create_booking(
    flight_offer: Dict[str, Any],
    travelers: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Create a flight booking using Amadeus API
    """
    return create_amadeus_booking(flight_offer, travelers)

def get_booking(booking_id: str) -> Optional[Dict[str, Any]]:
    """
    Get booking details from Amadeus
    """
    return get_booking_details(booking_id)

def cancel_booking(booking_id: str) -> bool:
    """
    Cancel a booking using Amadeus
    """
    return cancel_amadeus_booking(booking_id)

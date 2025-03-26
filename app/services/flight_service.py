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

def search_locations(keyword: str, location_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search for airports and cities based on a keyword.

    Args:
        keyword: The search term to find matching airports/cities.
        location_type: Optional filter for location type. Can be "AIRPORT", "CITY", or None for both.

    Returns:
        List of dictionaries containing location information
    """
    return search_airports_cities(keyword, location_type)

def get_flight_destinations(origin: str) -> List[Dict[str, Any]]:
    """Get all direct flight destinations from a given origin airport.

    Args:
        origin: IATA code of the origin airport (e.g., "BOM" for Mumbai).

    Returns:
        List of dictionaries containing destination information
    """
    return get_flight_destinations_amadeus(origin)

def search_flights(
    origin: str,
    destination: str,
    departure_date: datetime,
    adults: int,
) -> List[Dict[str, Any]]:
    """Search for available flights using the Amadeus API.

    Args:
        origin: IATA code of the departure airport.
        destination: IATA code of the arrival airport.
        departure_date: Date of departure.
        adults: Number of adult passengers (1-9).

    Returns:
        List of flight offers. Each offer is a dictionary containing detailed flight information
    """
    return search_flights_amadeus(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        adults=adults,
    )

def get_flight_offer_price(flight_offer: Dict[str, Any]) -> Dict[str, Any]:
    """Get the final price for a flight offer including taxes and fees.

    Args:
        flight_offer: A flight offer object returned from search_flights.

    Returns:
        Dictionary containing the pricing details
    """
    return get_flight_offer_price_amadeus(flight_offer)

def create_booking(
    flight_offer: Dict[str, Any],
    travelers: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Create a flight booking using the provided flight offer and traveler details.

    Args:
        flight_offer: A flight offer object returned from search_flights.
        travelers: List of traveler details including personal and document information.
            Each traveler should have fields like 'id', 'dateOfBirth', 'name',
            'contact', etc. See Amadeus documentation for full structure.

    Returns:
        Dictionary containing the booking confirmation details
    """
    return create_amadeus_booking(flight_offer, travelers)

def get_booking(booking_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve details of an existing booking.

    Args:
        booking_id: The unique identifier of the booking.

    Returns:
        Dictionary containing the booking details if found, None otherwise.
    """
    return get_booking_details(booking_id)

def cancel_booking(booking_id: str) -> bool:
    """Cancel an existing flight booking.

    Args:
        booking_id: The unique identifier of the booking to cancel.

    Returns:
        True if the booking was successfully cancelled, False otherwise.
    """
    return cancel_amadeus_booking(booking_id)

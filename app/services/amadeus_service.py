from datetime import datetime
from typing import List, Optional, Dict, Any
from app.config.amadeus_config import amadeus, handle_amadeus_error
from amadeus import ResponseError, Location
from app.utils.logger import get_logger

logger = get_logger(__name__)

def search_airports_cities(
    keyword: str,
    subtype: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search for airports and cities using Amadeus Location API.

    Args:
        keyword: Search term to find matching airports/cities.
        subtype: Optional filter for location type. Can be:
            - "AIRPORT": Only search for airports
            - "CITY": Only search for cities
            - None: Search for both airports and cities

    Returns:
        List of location dictionaries
    """
    try:
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType=subtype or Location.ANY
        )
        return response.data
    except ResponseError as error:
        handle_amadeus_error(error)
        return []

def get_flight_destinations(origin: str) -> List[Dict[str, Any]]:
    """Get all direct flight destinations from a given origin airport.

    Args:
        origin: IATA code of the origin airport (e.g., "BOM" for Mumbai)

    Returns:
        List of destination dictionaries
    """
    try:
        response = amadeus.airport.direct_destinations.get(departureAirportCode=origin)
        return response.data
    except ResponseError as error:
        handle_amadeus_error(error)
        return []

def search_flights(
    origin: str,
    destination: str,
    departure_date: datetime,
    adults: int,
    currency_code: str = "INR",
    max_results: int = 20
) -> List[Dict[str, Any]]:
    """Search for available flights using the Amadeus Flight Offers Search API.

    Args:
        origin: IATA code of the departure airport
        destination: IATA code of the arrival airport
        departure_date: Date of departure
        adults: Number of adult passengers (1-9)
        currency_code: Currency for pricing (default: "INR")
        max_results: Maximum number of results to return (default: 20)

    Returns:
        List of flight offer dictionaries
    """
    try:
        departure_date_str = departure_date.strftime("%Y-%m-%d")

        search_params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date_str,
            "adults": adults,
            "currencyCode": currency_code,
            "max": max_results,
        }

        response = amadeus.shopping.flight_offers_search.get(**search_params)
        return response.data

    except ResponseError as error:
        handle_amadeus_error(error)
        return []

def get_flight_offer_price(flight_offer: Dict[str, Any]) -> Dict[str, Any]:
    """Get the final price for a flight offer including taxes and fees.

    Args:
        flight_offer: A flight offer object returned from search_flights

    Returns:
        Dictionary containing pricing details
    """
    try:
        response = amadeus.shopping.flight_offers.pricing.post(flight_offer)
        return response.data
    except ResponseError as error:
        handle_amadeus_error(error)
        return {}

def create_flight_booking(
    flight_offer: Dict[str, Any],
    travelers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a flight booking using the Flight Create Orders API.

    Args:
        flight_offer: A flight offer object returned from search_flights
        travelers: List of traveler details.

    Returns:
        Dictionary containing booking details
    """
    try:
        response = amadeus.booking.flight_orders.post(
            flight_offer,
            travelers=travelers
        )
        return response.data
    except ResponseError as error:
        handle_amadeus_error(error)
        return {}

def get_booking_details(booking_id: str) -> Dict[str, Any]:
    """Retrieve booking details using the Flight Order Management API.

    Args:
        booking_id: The unique identifier of the booking

    Returns:
        Dictionary containing booking details
    """
    try:
        response = amadeus.booking.flight_order(booking_id).get()
        return response.data
    except ResponseError as error:
        handle_amadeus_error(error)
        return {}

def cancel_booking(booking_id: str) -> bool:
    """Cancel a flight booking.

    Args:
        booking_id: The unique identifier of the booking to cancel

    Returns:
        True if the booking was successfully cancelled, False otherwise
    """
    try:
        amadeus.booking.flight_order(booking_id).delete()
        return True
    except ResponseError as error:
        handle_amadeus_error(error)
        return False

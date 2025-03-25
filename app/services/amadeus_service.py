from datetime import datetime
from typing import List, Optional, Dict, Any
from app.config.amadeus_config import amadeus, handle_amadeus_error
from amadeus import ResponseError, Location
from app.utils.logger import get_logger

logger = get_logger(__name__)

def search_airports_cities(
    keyword: str,
    subtype: Optional[str] = None
) -> List[dict]:
    """
    Search for airports and cities (autocomplete)
    subtype can be: AIRPORT, CITY, or None for both
    """
    try:
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType=subtype or Location.ANY
        )
        locations = response.data
        return locations
    except ResponseError as error:
        handle_amadeus_error(error)
        return []

def get_flight_destinations(origin: str) -> List[dict]:
    """
    Get flight destinations from an origin
    """
    try:
        response = amadeus.airport.direct_destinations.get(departureAirportCode=origin)
        destinations = response.data
        return destinations
    except ResponseError as error:
        handle_amadeus_error(error)
        return []

def search_flights(
    origin: str,
    destination: str,
    departure_date: datetime,
    adults: int,
    currency_code: Optional[str] = "INR",
    max_results: Optional[int] = 20
) -> List[dict]:
    """
    Search for flights using the Amadeus Flight Offers Search API
    """
    try:
        # Format dates as YYYY-MM-DD
        departure_date_str = departure_date.strftime("%Y-%m-%d")

        # Prepare the search parameters
        search_params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date_str,
            "adults": adults,
            "currencyCode": currency_code,
            "max": max_results,
        }

        response = amadeus.shopping.flight_offers_search.get(**search_params)

        flights = response.data
        return flights

    except ResponseError as error:
        handle_amadeus_error(error)
        return []

def get_flight_offer_price(
    flight_offer: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Get the price of a flight offer
    """
    try:
        response = amadeus.shopping.flight_offers.pricing.post(flight_offer)
        flight_offer_price = response.data
        return flight_offer_price
    except ResponseError as error:
        handle_amadeus_error(error)
        return {}

def create_flight_booking(
    flight_offer: Dict[str, Any],
    travelers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create a flight booking using the Flight Create Orders API

    Travelers format:
    [{
      "id": "1",
      "dateOfBirth": "1982-01-16",
      "name": {
        "firstName": "JORGE",
        "lastName": "GONZALES"
      },
      "gender": "MALE",
      "contact": {
        "emailAddress": "jorge.gonzales833@telefonica.es",
        "phones": [
          {
            "deviceType": "MOBILE",
            "countryCallingCode": "34",
            "number": "480080076"
          }
        ]
      },
      "documents": [
        {
          "documentType": "PASSPORT",
          "birthPlace": "Madrid",
          "issuanceLocation": "Madrid",
          "issuanceDate": "2015-04-14",
          "number": "00000000",
          "expiryDate": "2025-04-14",
          "issuanceCountry": "ES",
          "validityCountry": "ES",
          "nationality": "ES",
          "holder": true
        }
      ]
    }]
    """
    try:
        response = amadeus.booking.flight_orders.post(
            flight_offer,
            travelers=travelers
        )
        booking = response.data
        return booking
    except ResponseError as error:
        handle_amadeus_error(error)
        return {}

def get_booking_details(booking_id: str) -> Dict[str, Any]:
    """
    Retrieve booking details using the Flight Order Management API
    """
    try:
        response = amadeus.booking.flight_order(booking_id).get()
        booking = response.data
        return booking
    except ResponseError as error:
        handle_amadeus_error(error)
        return {}

def cancel_booking(booking_id: str) -> bool:
    """
    Cancel a flight booking
    """
    try:
        amadeus.booking.flight_order(booking_id).delete()
        return True
    except ResponseError as error:
        handle_amadeus_error(error)
        return False

from datetime import datetime
from typing import Dict, List, Any, Optional, Literal
from mcp.server.fastmcp import FastMCP

from app.services import flight_service

# Create a FastMCP instance
mcp = FastMCP("Flight Booking MCP Server")

@mcp.tool()
def search_locations(
    keyword: str,
    type: Optional[Literal["AIRPORT", "CITY"]] = None
) -> List[Dict[str, Any]]:
    """
    Search for airports and cities based on a keyword.
    Results can be filtered by type (AIRPORT or CITY).
    Returns a list of locations with details like IATA code, name, and address.
    """
    return flight_service.search_locations(keyword, type)

@mcp.tool()
def get_flight_destinations(origin: str) -> List[Dict[str, Any]]:
    """
    Get all direct flight destinations from a given origin airport IATA code (e.g., 'BOM').
    Returns a list of destinations with details like distance and destination information.
    """
    return flight_service.get_flight_destinations(origin)

@mcp.tool()
def search_flights(
    origin: str,
    destination: str,
    departure_date: datetime,
    adults: int = 1
) -> List[Dict[str, Any]]:
    """
    Search for available flights based on origin, destination, departure date, and number of adults.
    Returns detailed flight information including prices, itineraries, and booking conditions.
    Number of adults must be between 1 and 9. Returns empty list if input is invalid.
    """
    if adults < 1 or adults > 9:
        return []
    return flight_service.search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        adults=adults,
    )

@mcp.tool()
def get_booking(booking_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve details of an existing booking using its unique identifier.
    Returns comprehensive booking information or an object indicating 'not_found' status.
    """
    booking = flight_service.get_booking(booking_id)
    if not booking:
        return {"status": "not_found", "booking_id": booking_id}
    return booking


@mcp.tool()
def get_flight_offer_price(flight_offer: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get the final price for a specific flight offer obtained from flight search results.
    Takes a flight offer object and returns the final pricing details including taxes and fees.
    """
    return flight_service.get_flight_offer_price(flight_offer)

@mcp.tool()
def create_booking(
    flight_offer: Dict[str, Any],
    travelers: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """
    Create a flight booking using a specific flight offer and traveler details.
    Traveler details must include required information (name, contact, documents).
    Returns booking confirmation details or null if booking failed.
    """
    booking = flight_service.create_booking(
        flight_offer=flight_offer,
        travelers=travelers,
    )
    if not booking:
        return {"status": "failed", "message": "Booking creation failed."}
    return booking

@mcp.tool()
def cancel_booking(booking_id: str) -> Dict[str, Any]:
    """
    Cancel an existing flight booking using its unique identifier.
    Returns the cancellation status. Check the 'status' field in the result.
    """
    success = flight_service.cancel_booking(booking_id)
    if not success:
        return {"status": "failed", "booking_id": booking_id, "message": "Could not cancel booking."}
    return {"status": "cancelled", "booking_id": booking_id}

if __name__ == "__main__":
    mcp.run(transport="sse")

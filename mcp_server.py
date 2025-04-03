from datetime import datetime
from typing import Dict, List, Any, Optional, Literal
from mcp.server.fastmcp import FastMCP

from app.services import flight_service
# from app.utils.logger import get_logger

# Initialize logger
# logger = get_logger(__name__)

# Create a FastMCP instance
mcp = FastMCP("Flight Booking MCP Server")

# --- Tools ---

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
    # logger.info("MCP Tool: Searching locations for keyword '%s', type '%s'", keyword, type)
    return flight_service.search_locations(keyword, type)

@mcp.tool()
def get_flight_destinations(origin: str) -> List[Dict[str, Any]]:
    """
    Get all direct flight destinations from a given origin airport IATA code (e.g., 'BOM').
    Returns a list of destinations with details like distance and destination information.
    """
    # logger.info("MCP Tool: Getting flight destinations from origin '%s'", origin)
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
        # logger.warning("MCP Tool: Invalid number of adults (%d) for flight search.", adults)
        return []
    # logger.info(
    #     "MCP Tool: Searching flights from %s to %s on %s for %d adults",
    #     origin, destination, departure_date, adults
    # )
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
    # logger.info("MCP Tool: Getting booking details for ID '%s'", booking_id)
    booking = flight_service.get_booking(booking_id)
    if not booking:
        # logger.warning("MCP Tool: Booking not found for ID '%s'", booking_id)
        return {"status": "not_found", "booking_id": booking_id}
    return booking


# --- Tools ---

@mcp.tool()
def get_flight_offer_price(flight_offer: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get the final price for a specific flight offer obtained from flight search results.
    Takes a flight offer object and returns the final pricing details including taxes and fees.
    """
    # logger.info("MCP Tool: Getting price for flight offer ID '%s'", flight_offer.get('id', 'N/A'))
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
    # logger.info(
    #     "MCP Tool: Creating booking for flight offer ID '%s' with %d travelers",
    #     flight_offer.get("id", "N/A"), len(travelers)
    # )
    booking = flight_service.create_booking(
        flight_offer=flight_offer,
        travelers=travelers,
    )
    if not booking:
        # logger.error(
        #     "MCP Tool: Failed to create booking for flight offer ID '%s'",
        #      flight_offer.get("id", "N/A")
        # )
        return {"status": "failed", "message": "Booking creation failed."}
    # logger.info("MCP Tool: Booking created successfully with ID '%s'", booking.get("id"))
    return booking

@mcp.tool()
def cancel_booking(booking_id: str) -> Dict[str, Any]:
    """
    Cancel an existing flight booking using its unique identifier.
    Returns the cancellation status. Check the 'status' field in the result.
    """
    # logger.info("MCP Tool: Attempting to cancel booking ID '%s'", booking_id)
    success = flight_service.cancel_booking(booking_id)
    if not success:
        # logger.error("MCP Tool: Failed to cancel booking ID '%s'", booking_id)
        return {"status": "failed", "booking_id": booking_id, "message": "Could not cancel booking."}
    # logger.info("MCP Tool: Booking ID '%s' cancelled successfully", booking_id)
    return {"status": "cancelled", "booking_id": booking_id}

# You can run this server using:
# mcp dev app/mcp_server.py
# or integrate it into your main application if needed.

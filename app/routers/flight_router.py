from fastapi import APIRouter, HTTPException, Query, Path, status
from datetime import datetime
from typing import List, Literal, Optional, Dict, Any

from app.services import flight_service
from app.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

router = APIRouter(
    prefix="/flights",
    tags=["Flights"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)

@router.get(
    "/locations/search",
    response_model=List[Dict[str, Any]],
    summary="Search for airports and cities",
    response_description="List of matching airports and cities",
)
def search_locations(
    keyword: str = Query(..., description="Search term to find matching airports/cities"),
    type: Optional[Literal["AIRPORT", "CITY"]] = Query(
        None,
        description="Filter results by location type. Leave empty to search both airports and cities",
    ),
):
    """Search for airports and cities based on a keyword.

    The search is performed using the Amadeus Location API and returns matching
    airports and cities based on the provided keyword. Results can be filtered
    by type (AIRPORT or CITY).

    Returns a list of locations with details like IATA code, name, and address.
    """
    return flight_service.search_locations(keyword, type)

@router.get(
    "/destinations",
    response_model=List[Dict[str, Any]],
    summary="Get direct flight destinations",
    response_description="List of destinations with direct flights",
)
def get_flight_destinations(
    origin: str = Query(..., description="IATA code of the origin airport (e.g., 'BOM' for Mumbai)"),
):
    """Get all direct flight destinations from a given origin airport.

    Returns a list of destinations that can be reached via direct flights
    from the specified origin airport, including details like distance
    and destination information.
    """
    return flight_service.get_flight_destinations(origin)

@router.get(
    "/search",
    response_model=List[Dict[str, Any]],
    summary="Search for available flights",
    response_description="List of available flight offers",
)
def search_flights(
    origin: str = Query(..., description="IATA code of the departure airport"),
    destination: str = Query(..., description="IATA code of the arrival airport"),
    departure_date: datetime = Query(..., description="Date of departure (YYYY-MM-DD)"),
    adults: int = Query(
        default=1,
        ge=1,
        le=9,
        description="Number of adult passengers (1-9)",
    ),
):
    """Search for available flights based on the provided criteria.

    This endpoint searches for flight offers matching the specified origin,
    destination, date, and number of passengers. It returns detailed flight
    information including prices, itineraries, and booking conditions.

    Raises:
        HTTPException(400): If the number of adults is less than 1 or greater than 9
    """
    if adults < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of adults must be at least 1",
        )
    if adults > 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum number of adults is 9",
        )

    logger.info("Searching flights from %s to %s on %s", origin, destination, departure_date)
    flights = flight_service.search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        adults=adults,
    )
    logger.info("Found %d flights for %s to %s on %s", len(flights), origin, destination, departure_date)
    return flights

@router.post(
    "/offer-price",
    response_model=Dict[str, Any],
    summary="Get final price for a flight offer",
    response_description="Flight offer with final pricing details",
)
def get_flight_offer_price(
    flight_offer: Dict[str, Any],
):
    """Get the final price for a flight offer including all taxes and fees.

    Takes a flight offer from the search results and returns the final pricing
    details including base fare, taxes, and total amount in the requested currency.
    """
    return flight_service.get_flight_offer_price(flight_offer)

@router.post(
    "/bookings",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new flight booking",
    response_description="Booking confirmation details",
)
def create_booking(
    flight_offer: Dict[str, Any],
    travelers: List[Dict[str, Any]],
):
    """Create a flight booking using the provided flight offer and traveler details.

    Creates a confirmed booking for the specified flight offer and travelers.
    Traveler details must include all required information such as name,
    contact details, and travel documents.

    Raises:
        HTTPException(400): If the booking could not be created
    """
    logger.info(
        "Creating new booking",
        extra={
            "flight_offer_id": flight_offer.get("id"),
            "travelers": len(travelers),
        },
    )
    booking = flight_service.create_booking(
        flight_offer=flight_offer,
        travelers=travelers,
    )
    if not booking:
        logger.error(
            "Failed to create booking",
            extra={"flight_offer_id": flight_offer.get("id")},
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create booking",
        )
    logger.info("Booking created successfully", extra={"booking_id": booking.get("id")})
    return booking

@router.get(
    "/bookings/{booking_id}",
    response_model=Dict[str, Any],
    summary="Get booking details",
    response_description="Detailed booking information",
)
def get_booking(
    booking_id: str = Path(..., description="Unique identifier of the booking"),
):
    """Retrieve details of an existing booking.

    Returns comprehensive booking information including flight details,
    passenger information, and booking status.

    Raises:
        HTTPException(404): If the booking is not found
    """
    booking = flight_service.get_booking(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    return booking

@router.delete(
    "/bookings/{booking_id}",
    status_code=status.HTTP_200_OK,
    summary="Cancel a booking",
    response_description="Booking cancellation status",
)
def cancel_booking(
    booking_id: str = Path(..., description="Unique identifier of the booking to cancel"),
):
    """Cancel an existing flight booking.

    Attempts to cancel the specified booking and returns the cancellation status.

    Raises:
        HTTPException(404): If the booking could not be cancelled
    """
    success = flight_service.cancel_booking(booking_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not cancel booking",
        )
    return {"status": "cancelled", "booking_id": booking_id}

from fastapi import APIRouter, HTTPException, Query, status
from datetime import datetime
from typing import List, Literal, Optional, Dict, Any

from app.services import flight_service
from app.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

router = APIRouter(
    prefix="/flights",
    tags=["Flights"],
    responses={404: {"description": "Not found"}},
)

@router.get("/locations/search", response_model=List[Dict[str, Any]])
def search_locations(
    keyword: str,
    type: Optional[Literal["AIRPORT", "CITY"]] = None
):
    """
    Search for airports and cities
    type can be: AIRPORT, CITY, or None for both
    """
    return flight_service.search_locations(keyword, type)

@router.get("/destinations", response_model=List[Dict[str, Any]])
def get_flight_destinations(
    origin: str
):
    """
    Get direct flight destinations from an origin
    """
    return flight_service.get_flight_destinations(origin)

@router.get("/search", response_model=List[Dict[str, Any]])
def search_flights(
    origin: str,
    destination: str,
    departure_date: datetime,
    adults: int = Query(default=1, ge=1, le=9)
):
    """
    Search for flights by origin, destination, and departure date
    """
    if adults is not None:
        if adults < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Number of adults must be at least 1"
            )
        if adults > 9:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum number of adults is 9"
            )

    logger.info("Searching flights from %s to %s on %s", origin, destination, departure_date)
    flights = flight_service.search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        adults=adults
    )
    logger.info("Found %d flights for %s to %s on %s", len(flights), origin, destination, departure_date)
    return flights

@router.post("/offer-price", response_model=Dict[str, Any])
def get_flight_offer_price(
    flight_offer: Dict[str, Any]
):
    """
    Get the price of a flight offer
    """
    return flight_service.get_flight_offer_price(flight_offer)

@router.post("/bookings", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_booking(
    flight_offer: Dict[str, Any],
    travelers: List[Dict[str, Any]]
):
    """
    Create a flight booking
    """
    logger.info("Creating new booking", extra={
        "flight_offer_id": flight_offer.get("id"),
        "travelers": len(travelers)
    })
    booking = flight_service.create_booking(
        flight_offer=flight_offer,
        travelers=travelers
    )
    if not booking:
        logger.error("Failed to create booking", extra={
            "flight_offer_id": flight_offer.get("id")
        })
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create booking"
        )
    logger.info("Booking created successfully", extra={"booking_id": booking.get("id")})
    return booking

@router.get("/bookings/{booking_id}", response_model=Dict[str, Any])
def get_booking(booking_id: str):
    """
    Get booking details
    """
    booking = flight_service.get_booking(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return booking

@router.delete("/bookings/{booking_id}", status_code=status.HTTP_200_OK)
def cancel_booking(booking_id: str):
    """
    Cancel a booking
    """
    success = flight_service.cancel_booking(booking_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not cancel booking"
        )
    return {"status": "cancelled", "booking_id": booking_id}

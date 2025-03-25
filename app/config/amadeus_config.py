from amadeus import Client, ResponseError
from dotenv import load_dotenv
import os
from fastapi import HTTPException

load_dotenv()

amadeus = Client(
    client_id=os.getenv('AMADEUS_CLIENT_ID'),
    client_secret=os.getenv('AMADEUS_CLIENT_SECRET'),
    hostname='test'
)

def handle_amadeus_error(error: ResponseError):
    """Handle Amadeus API errors and convert them to FastAPI HTTP exceptions"""
    if error.response.status_code == 401:
        raise HTTPException(status_code=401, detail="Authentication failed with Amadeus API")
    elif error.response.status_code == 404:
        raise HTTPException(status_code=404, detail="Resource not found in Amadeus API")
    else:
        raise HTTPException(
            status_code=error.response.status_code,
            detail=f"Amadeus API error: {error.response.body}"
        )

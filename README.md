# Flight Booking API

A FastAPI-based flight booking API that integrates with the Amadeus Travel API to provide flight searching, pricing, booking, and management capabilities.

## Setup

1. Create a virtual environment:
```bash
uv venv .venv --python 3.12
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv pip sync requirements.txt
```

4. Set up Amadeus API credentials (required):
   - Create an account at [Amadeus for Developers](https://developers.amadeus.com/)
   - Get API Key and API Secret
   - Set environment variables:
     ```bash
     export AMADEUS_CLIENT_ID=your_api_key
     export AMADEUS_CLIENT_SECRET=your_api_secret
     ```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

The server will start at http://localhost:8000

## API Endpoints

### Flight Management
- `GET /flights/locations/search` - Search for airports and cities
- `GET /flights/destinations` - Get direct flight destinations from an origin
- `GET /flights/search` - Search for available flights
- `POST /flights/offer-price` - Get final price for a flight offer

### Booking Management
- `POST /flights/bookings` - Create a new flight booking
- `GET /flights/bookings/{booking_id}` - Get booking details
- `DELETE /flights/bookings/{booking_id}` - Cancel a booking

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Detailed API documentation: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## Technology Stack

- FastAPI: Web framework
- Amadeus Travel API: Flight data and booking management
- UVicorn: ASGI server
- Python 3.12+

# Flight Booking API

A simple FastAPI-based flight booking server that manages flight searches, bookings, and cancellations.

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

4. Run the server:
```bash
uvicorn app.main:app --reload
```

The server will start at http://localhost:8000

## API Endpoints

- `GET /flights/search` - Search for flights
- `GET /flights/{flight_id}` - Get flight details
- `POST /bookings` - Create a new booking
- `GET /bookings/{booking_id}` - Get booking details
- `DELETE /bookings/{booking_id}` - Cancel a booking

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

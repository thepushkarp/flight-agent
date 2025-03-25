# Flight Booking API Documentation

## Server Information
- Base URL: `https://0bf0-202-140-45-108.ngrok-free.app`
- Interactive API Documentation (Swagger UI): `https://0bf0-202-140-45-108.ngrok-free.app/docs`
- OpenAPI Specification: `https://0bf0-202-140-45-108.ngrok-free.app/openapi.json`

## Overview
This API provides endpoints for managing flight bookings, including searching flights, creating bookings, and managing passenger information. For now, this API uses a dummy database for creating and managing bookings.

## Common Response Codes
- `200 OK`: Request successful
- `201 Created`: Resource successfully created
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Requested resource not found
- `500 Internal Server Error`: Server-side error

## Endpoints

### 1. List All Flights
Retrieves a list of all available flights.

**Endpoint:** `GET /flights`

**Response:** Array of Flight objects
```json
[
  {
    "id": "string",
    "flight_number": "string",
    "origin": "string",
    "destination": "string",
    "departure_time": "string (ISO 8601 datetime)",
    "arrival_time": "string (ISO 8601 datetime)",
    "available_seats": "integer",
    "price": "float",
    "flight_class": "string",
    "airline": "string"
  }
]
```

### 2. Search Flights
Search for flights based on specific criteria. All parameters are optional - if none are provided, returns all flights.

**Endpoint:** `GET /flights/search`

**Query Parameters:**
- `origin` (string, optional): Departure city/airport code (e.g., "JFK", "LAX")
- `destination` (string, optional): Arrival city/airport code (e.g., "LHR", "SFO")
- `departure_date` (string, optional): Departure date in ISO 8601 format (YYYY-MM-DD)
- `flight_class` (string, optional): Class of travel (e.g., "ECONOMY", "BUSINESS", "FIRST")
- `adults` (integer, optional): Number of adult passengers

**Response:** Array of matching Flight objects
```json
[
  {
    "id": "string",
    "flight_number": "string",
    "origin": "string",
    "destination": "string",
    "departure_time": "string (ISO 8601 datetime)",
    "arrival_time": "string (ISO 8601 datetime)",
    "available_seats": "integer",
    "price": "float",
    "flight_class": "string",
    "airline": "string"
  }
]
```

**Example Usage:**
```http
# Full search with all parameters
GET /flights/search?origin=NYC&destination=LON&departure_date=2024-04-01&adults=2&flight_class=ECONOMY

# Search by route only
GET /flights/search?origin=NYC&destination=LON

# Search by departure date only
GET /flights/search?departure_date=2024-04-01
```

### 3. Get Flight Details
Retrieve details for a specific flight.

**Endpoint:** `GET /flights/{flight_id}`

**Path Parameters:**
- `flight_id` (string, required): Unique identifier of the flight

**Response:** Single Flight object
```json
{
  "id": "string",
  "flight_number": "string",
  "origin": "string",
  "destination": "string",
  "departure_time": "string (ISO 8601 datetime)",
  "arrival_time": "string (ISO 8601 datetime)",
  "available_seats": "integer",
  "price": "float",
  "flight_class": "string",
  "airline": "string"
}
```

### 4. List All Bookings
Retrieve all bookings in the system.

**Endpoint:** `GET /bookings`

**Response:** Array of Booking objects
```json
[
  {
    "id": "string",
    "flight_id": "string",
    "booking_status": "string",
    "contact_email": "string",
    "contact_phone": "string",
    "passengers": [
      {
        "first_name": "string",
        "last_name": "string",
        "passport_number": "string",
        "date_of_birth": "string (ISO 8601 date)"
      }
    ]
  }
]
```

### 5. Create Booking
Create a new flight booking.

**Endpoint:** `POST /bookings`

**Request Body:**
```json
{
  "flight_id": "string (required)",
  "contact_email": "string (required)",
  "contact_phone": "string (required)",
  "passengers": [
    {
      "first_name": "string (required)",
      "last_name": "string (required)",
      "passport_number": "string (required)",
      "date_of_birth": "string (required, ISO 8601 date)"
    }
  ]
}
```

**Response:** Created Booking object (status code: 201)

### 6. Get Booking Details
Retrieve details for a specific booking.

**Endpoint:** `GET /bookings/{booking_id}`

**Path Parameters:**
- `booking_id` (string, required): Unique identifier of the booking

**Response:** Single Booking object
```json
{
  "id": "string",
  "flight_id": "string",
  "booking_status": "string",
  "contact_email": "string",
  "contact_phone": "string",
  "passengers": [
    {
      "first_name": "string",
      "last_name": "string",
      "passport_number": "string",
      "date_of_birth": "string (ISO 8601 date)"
    }
  ]
}
```

### 7. Cancel Booking
Cancel an existing booking.

**Endpoint:** `DELETE /bookings/{booking_id}`

**Path Parameters:**
- `booking_id` (string, required): Unique identifier of the booking to cancel

**Response:** The cancelled Booking object

### 8. List All Passengers
Retrieve all passengers in the system.

**Endpoint:** `GET /passengers`

**Response:** Array of PassengerInfo objects
```json
[
  {
    "first_name": "string",
    "last_name": "string",
    "passport_number": "string",
    "date_of_birth": "string (ISO 8601 date)"
  }
]
```

## Data Types and Formats

### DateTime Format
All datetime fields should be provided in ISO 8601 format:
- Date only: `YYYY-MM-DD`
- DateTime: `YYYY-MM-DDTHH:mm:ss.sssZ`

### Flight Classes
Valid flight classes include:
- ECONOMY
- BUSINESS
- FIRST

### Booking Status
Possible booking status values:
- CONFIRMED
- CANCELLED

## Error Responses
When an error occurs, the API will return an error object:
```json
{
  "detail": "string (error message describing what went wrong)"
}
```

## Integration Guidelines for LLMs

### Best Practices
1. Always validate input parameters before making requests
2. Handle all possible HTTP status codes appropriately
3. Ensure datetime strings are properly formatted in ISO 8601
4. When creating bookings, ensure all required passenger information is provided
5. Phone numbers should include country code
6. Email addresses should be properly formatted
7. Passport numbers should be provided exactly as they appear on the passport
8. For search operations, while all parameters are optional, providing more parameters will help narrow down the results

### Example Usage

1. Searching for flights (various examples):
```http
# Full search with all parameters
GET https://0bf0-202-140-45-108.ngrok-free.app/flights/search?origin=NYC&destination=LON&departure_date=2024-04-01&adults=2&flight_class=ECONOMY

# Search by route only
GET https://0bf0-202-140-45-108.ngrok-free.app/flights/search?origin=NYC&destination=LON

# Search by departure date only
GET https://0bf0-202-140-45-108.ngrok-free.app/flights/search?departure_date=2024-04-01
```

2. Creating a booking:
```http
POST https://0bf0-202-140-45-108.ngrok-free.app/bookings
Content-Type: application/json

{
  "flight_id": "FL123",
  "contact_email": "passenger@example.com",
  "contact_phone": "+1234567890",
  "passengers": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "passport_number": "P123456789",
      "date_of_birth": "1990-01-01"
    }
  ]
}
```

## Additional Resources
- Interactive API Documentation: Visit the [Swagger UI](https://0bf0-202-140-45-108.ngrok-free.app/docs) for interactive API testing
- OpenAPI Specification: Download the [OpenAPI JSON](https://0bf0-202-140-45-108.ngrok-free.app/openapi.json) for automated tooling

## Notes
- The API is currently running on an ngrok tunnel, which means the URL may change in the future
- For production use, ensure proper error handling, rate limiting, and authentication mechanisms are implemented
- All endpoints return JSON responses
- Request bodies must be sent with Content-Type: application/json header

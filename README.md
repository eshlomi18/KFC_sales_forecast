# KFC Sales Forecast System - Backend API

This is a Backend service designed to forecast future sales for KFC branches based on historical data. It's built with Python, FastAPI, and MongoDB, and is fully containerized using Docker.

## Tech Stack
* **Framework:** FastAPI (Python)
* **Database:** MongoDB (Async with motor)
* **Data Validation:** Pydantic (Using different models for database storage and API responses)
* **Deployment:** Docker & Docker Compose
* **Logging:** loguru

## Core Components
1. **API (main.py):** Serves the forecast data to the frontend. Includes filtering (by store, product, date), sorting, and pagination.
2. **Database Seeder (seed.py):** Automatically injects mock historical sales data on the first run so the generator has data to work with.
3. **Background Worker (forecast_generator.py):** Runs continuously in the background. It calculates the average of historical sales to generate a forecast for the next day.

## How to Run
Ensure you have Docker and Docker Compose installed.

1. Clone the repository.
2. Open a terminal in the project directory and run:
   docker-compose up --build
3. The API will be available at: http://localhost:8000
4. API Documentation (Swagger UI): http://localhost:8000/docs
5. MongoDB Express Dashboard: http://localhost:8081 (User: admin, Pass: pass)

## Endpoints

### GET /
Health check status.

### GET /api/forecasts
Retrieves the generated forecasts.

**Query Parameters:**
* `skip` (int): For pagination (default: 0).
* `limit` (int): Max records per request (default: 100).
* `store_id` (str, optional): Filter by Store ID.
* `product_name` (str, optional): Filter by Product Name.
* `forecast_date` (str, optional): Filter by exact date (format: YYYY-MM-DD).

**Response:**
Returns a JSON object containing the `forecasts` array, pagination details, and the `total_count` of matched records.
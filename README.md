# KFC Sales Forecast System - Backend API

This project is a robust Backend service designed to forecast future sales for KFC branches based on historical data. It is built with a modern Python stack and fully containerized using Docker.

## Architecture & Tech Stack
* **Framework:** FastAPI (Python)
* **Database:** MongoDB (Async via motor)
* **Deployment:** Docker & Docker Compose
* **Logging:** loguru for structured terminal logs

## Core Components
1. **API (main.py):** Serves the data to the client. Includes pagination logic (skip and limit) to handle large datasets efficiently.
2. **Database Seeder (seed.py):** Automatically injects 500 records of randomized historical sales data and branch information on the first run.
3. **Background Worker (forcast_generator.py):** Runs continuously in the background via FastAPI's lifespan events. It calculates a 7-day average of historical sales to generate predictive forecasts every 24 hours.

## How to Run
Ensure you have Docker and Docker Compose installed.

1. Clone the repository.
2. Open a terminal in the project directory and run:
   docker-compose up --build
3. The API will be available at: http://localhost:8000
4. Interactive API Documentation (Swagger UI): http://localhost:8000/docs
5. MongoDB Express Dashboard: http://localhost:8081 (User: admin, Pass: pass)

## Endpoints
* GET / : Health check status.
* GET /api/forecasts : Retrieves generated forecasts. Supports pagination:
    * skip: Number of records to skip (default: 0)
    * limit: Number of records to return (default: 100, max: 1000)
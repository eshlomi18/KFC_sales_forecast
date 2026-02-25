# KFC Sales Forecast System

This is a full-stack application designed to forecast future sales for KFC branches based on historical data. It includes a Python/FastAPI backend, a MongoDB database, and a React frontend for displaying the data. The entire system is containerized using Docker.

## Tech Stack
* **Frontend:** React, Vite, Material UI
* **Backend:** FastAPI (Python), Motor (Async MongoDB)
* **Database:** MongoDB
* **Deployment:** Docker & Docker Compose

## Core Components
1. **Frontend Dashboard:** A React UI that displays the sales forecasts in a table. It includes pagination and allows users to filter the data by Store ID and Date.
2. **Backend API:** A FastAPI application that serves the forecast data to the frontend, handling filtering, sorting, and pagination logic.
3. **Database Seeder (seed.py):** A script that generates initial mock historical sales data so the system has data to work with on the first run.
4. **Background Worker (forecast_generator.py):** A script that calculates the average of historical sales to generate a forecast for the next day.

## How to Run
Ensure you have Docker and Docker Compose installed on your machine.

1. Clone the repository to your local machine.
2. Open a terminal in the project directory.
3. Run the following command:
   docker-compose up --build -d

## Services & Ports
Once the containers are running, you can access the different services here:
* **Frontend Dashboard:** http://localhost:5173
* **Backend API:** http://localhost:8000
* **API Documentation (Swagger UI):** http://localhost:8000/docs
* **MongoDB Express (DB UI):** http://localhost:8081 (User: admin, Pass: pass)

## Main API Endpoint

### GET /api/forecasts
Retrieves the generated forecasts.

**Query Parameters:**
* `skip` (int): For pagination (default: 0).
* `limit` (int): Max records per request (default: 100).
* `store_id` (str, optional): Filter by Store ID.
* `forecast_date` (str, optional): Filter by exact date (format: YYYY-MM-DD).

**Response:**
Returns a JSON object containing the `forecasts` array and the `total_count` of matched records to support frontend pagination.
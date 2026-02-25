from datetime import datetime
from fastapi import FastAPI, Query
import asyncio
from contextlib import asynccontextmanager
from forecast_generator import forecast_loop
from loguru import logger
from database import forecasts_collection
from fastapi.middleware.cors import CORSMiddleware
from models import ForecastResponse
from typing import Optional


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI is starting up...")
    asyncio.create_task(forecast_loop())
    logger.success("Background forecast worker launched successfully!")

    yield

    logger.info("Shutting down KFC Forecast API. Cleaning up resources...")


app = FastAPI(title="KFC Sales Forecast API", lifespan=lifespan)
# This allows the local React frontend running on a different port to securely make HTTP requests to this FastAPI backend.
# In production, you would want to restrict this to specific origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "KFC Forecast API is running",
        "worker": "active"
    }


@app.get("/api/forecasts", response_model=ForecastResponse)
async def get_forecasts(
        skip: int = Query(0, description="How many records to skip (for pagination)"),
        limit: int = Query(100, le=1000, description="Max records to return per request"),
        store_id: Optional[str] = Query(None, description="Filter by store ID"),
        product_name: Optional[str] = Query(None, description="Filter by product name"),
        forecast_date: Optional[str] = Query(None, description="Filter by exact date (YYYY-MM-DD)")
):
    """
    Retrieve sales forecasts with optional filtering and pagination.

    - Filters are exact matches.
    - Results are sorted chronologically by date->hour->store->product.
    - Returns the paginated data along with the `total_count` of matched records.
    """
    logger.info("Fetching forecasts from database for client...")


    # Build the MongoDB Query Dynamically
    db_query = {}

    if store_id:
        db_query["store_id"] = store_id

    if product_name:
        db_query["product_name"] = product_name

    if forecast_date:
        try:
            # Convert string to datetime object for MongoDB
            parsed_date = datetime.strptime(forecast_date, "%Y-%m-%d")
            db_query["forecast_date"] = parsed_date
        except ValueError:
            logger.warning(f"Invalid date format received: {forecast_date}")


    # Count total documents for Pagination
    total_count = await forecasts_collection.count_documents(db_query)

    # Retrieve the requested page of results, ordered logically for the UI table
    cursor = (
        forecasts_collection.find(db_query, {"_id": 0})
        .sort([
            ("forecast_date", 1),
            ("hour", 1),
            ("store_id", 1),
            ("product_name", 1)
        ])
        .skip(skip)
        .limit(limit)
    )
    forecasts_data = await cursor.to_list(length=limit)

    # Construct the final JSON payload expected by the frontend
    return {
        "forecasts": forecasts_data,
        "total_count": total_count,
        "skip": skip,
        "limit": limit
    }
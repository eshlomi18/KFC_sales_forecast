from fastapi import FastAPI, Query
import asyncio
from contextlib import asynccontextmanager
from forcast_generator import forecast_loop
from loguru import logger
from database import forecasts_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI is starting up...")
    asyncio.create_task(forecast_loop())
    logger.success("Background forecast worker launched successfully!")

    yield

    logger.info("Shutting down KFC Forecast API. Cleaning up resources...")


app = FastAPI(title="KFC Sales Forecast API", lifespan=lifespan)


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "KFC Forecast API is running",
        "worker": "active"
    }


@app.get("/api/forecasts")
async def get_forecasts(
        skip: int = Query(0, description="How many records to skip (for pagination)"),
        limit: int = Query(100, le=1000, description="Max records to return per request")
):
    logger.info("Fetching forecasts from database for client...")
    # Exclude MongoDB '_id' because ObjectId is not natively JSON serializable
    cursor = forecasts_collection.find({}, {"_id": 0}).skip(skip).limit(limit)
    forecasts = await cursor.to_list(length=limit)

    return {
        "forecasts": forecasts,
        "skip": skip,
        "limit": limit
    }

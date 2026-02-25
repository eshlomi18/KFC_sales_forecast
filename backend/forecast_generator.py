import asyncio
from datetime import datetime, timedelta, timezone
from database import sales_collection, forecasts_collection
from config import settings
from models import SalesForecastDB
from loguru import logger


def get_calculation_dates():
    """
    Calculates the target date for the forecast (tomorrow) and the history start date.

    Aligning dates to midnight (00:00:00) ensures that our data window remains
    perfectly accurate even if the execution time drifts (e.g., due to retries).
    """
    now_utc = datetime.now(timezone.utc)
    today_midnight = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)

    target_date = today_midnight + timedelta(days=1)
    history_start_date = today_midnight - timedelta(days=settings.average_days_back)

    return target_date, history_start_date


async def fetch_sales_averages(history_start_date):
    """
    Queries MongoDB to filter recent days and calculate the average sales
    per store, product, and hour.

    Computation is intentionally offloaded to the database layer using MongoDB's
    Aggregation Pipeline. This minimizes network I/O and reduces memory consumption
    on the Python application side.
    """
    pipeline = [
        {"$match": {"sale_date": {"$gte": history_start_date}}},
        {"$group": {
            "_id": {
                "store_id": "$store_id",
                "product_name": "$product_name",
                "hour": "$hour"
            },
            "average_quantity": {"$avg": "$quantity"}
        }}
    ]

    # The aggregation pipeline runs entirely on the database side, doing all the heavy lifting.
    # It returns a cursor pointing to the grouped results, which are now small enough
    # to be safely loaded into the application's memory all at once.
    cursor = sales_collection.aggregate(pipeline)

    # Fetch data asynchronously and convert to a list in memory
    return await cursor.to_list(length=None)


async def save_forecasts(results, target_date):
    """
    Validates, rounds, and saves the calculated averages to the database.

    Idempotency handling: Delete existing forecasts for the target date before inserting.
    This ensures that even if the job runs multiple times (e.g., server restarts),
    we prevent data duplication and keep the database clean.

    """
    forecasts_to_insert = []

    for item in results:
        rounded_prediction = int(round(item["average_quantity"]))

        forecast = SalesForecastDB(
            store_id=item["_id"]["store_id"],
            product_name=item["_id"]["product_name"],
            hour=item["_id"]["hour"],
            forecast_date=target_date,
            predicted_sales=rounded_prediction
        )
        forecasts_to_insert.append(forecast.model_dump())

    if forecasts_to_insert:
        await forecasts_collection.delete_many({"forecast_date": target_date})
        await forecasts_collection.insert_many(forecasts_to_insert)
        logger.success(f"Successfully saved {len(forecasts_to_insert)} forecasts for {target_date.strftime('%Y-%m-%d')}.")


async def generate_daily_forecast():
    """
    Orchestrator function: handles dates calculation -> data fetching -> data saving.
    """
    logger.info(f"Starting generator: Calculating average from the last {settings.average_days_back} days...")

    target_date, history_start_date = get_calculation_dates()
    results = await fetch_sales_averages(history_start_date)

    if not results:
        logger.warning("No historical sales data found. Skipping forecast generation.")
        return

    await save_forecasts(results, target_date)


async def forecast_loop():
    """
    Background worker loop that triggers the forecast generation.

    Using a simple while/sleep loop for the scope of this assignment.
    In a real Production environment, this naive approach would be replaced by a dedicated
    task scheduler or background job queue to handle precise timing, state management,
    and catch-up executions if the server goes down.
    """
    logger.info(f"Forecast background task started. Interval: {settings.forecast_interval_hours} hours.")

    while True:
        try:
            # Attempt to run the core algorithm
            await generate_daily_forecast()

            sleep_duration = timedelta(hours=settings.forecast_interval_hours)
            logger.info(f"Generator going to sleep for {settings.forecast_interval_hours} hours...")
            await asyncio.sleep(sleep_duration.total_seconds())

        except Exception as e:
            # Fallback: sleep for 5 minutes before retrying to avoid infinite rapid loops
            logger.error(f"Error during forecast generation: {e}")
            logger.info("Retrying in 5 minutes...")
            await asyncio.sleep(300)


if __name__ == "__main__":
    asyncio.run(generate_daily_forecast())
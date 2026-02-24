import asyncio
import random
from datetime import datetime, timezone, timedelta
from loguru import logger
from database import stores_collection, sales_collection
from constants import (
    SEED_NUM_SALES, SEED_MIN_QTY, SEED_MAX_QTY,
    SEED_MIN_HOUR, SEED_MAX_HOUR, SEED_DAYS_BACK,
    PRODUCTS, STORES
)


async def seed_database():
    count = await stores_collection.count_documents({})
    if count > 0:
        logger.info("Database already contains data. Skipping seeding.")
        return

    logger.info(f"Starting database seeding process with {SEED_NUM_SALES} records...")
    now = datetime.now(timezone.utc)
    stores_data = STORES
    store_ids = [store["store_id"] for store in STORES]

    sales_data = []

    for _ in range(SEED_NUM_SALES):
        random_store = random.choice(store_ids)
        random_product = random.choice(PRODUCTS)
        random_hour = random.randint(SEED_MIN_HOUR, SEED_MAX_HOUR)
        random_quantity = random.randint(SEED_MIN_QTY, SEED_MAX_QTY)

        days_ago = random.randint(1, SEED_DAYS_BACK)
        random_date = now - timedelta(days=days_ago)

        sales_data.append({
            "store_id": random_store,
            "product_name": random_product,
            "hour": random_hour,
            "quantity": random_quantity,
            "sale_date": random_date
        })

    try:
        await stores_collection.insert_many(stores_data)
        await sales_collection.insert_many(sales_data)
        logger.success(f"Database seeded successfully with {len(sales_data)} historical sales records!")
    except Exception as e:
        logger.error(f"Failed to seed database. Error: {e}")


if __name__ == "__main__":
    asyncio.run(seed_database())
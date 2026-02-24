from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from constants import STORES_COLLECTION, FORECASTS_COLLECTION, SALES_COLLECTION, DB_NAME

# Using Motor (AsyncIOMotorClient) for non-blocking, asynchronous database operations,
# ensuring the FastAPI event loop remains responsive.
client = AsyncIOMotorClient(settings.mongo_url)
db = client[DB_NAME]

# Initialize collections
stores_collection = db.get_collection(STORES_COLLECTION)
forecasts_collection = db.get_collection(FORECASTS_COLLECTION)
sales_collection = db.get_collection(SALES_COLLECTION)
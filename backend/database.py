from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from constants import STORES_COLLECTION, FORECASTS_COLLECTION

# שימוש בכתובת המרוכזת
client = AsyncIOMotorClient(settings.mongo_url)
db = client.kfc_sales_forecast

# הגדרת הטבלאות
stores_collection = db.get_collection(STORES_COLLECTION)
forecasts_collection = db.get_collection(FORECASTS_COLLECTION)

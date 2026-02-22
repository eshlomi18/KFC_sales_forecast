import os
from motor.motor_asyncio import AsyncIOMotorClient

# Fetch the MongoDB connection string from environment variables
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Create the asynchronous MongoDB client
client = AsyncIOMotorClient(MONGO_URL)

# Select our specific database
db = client.kfc_sales_forecast

# Define the collections
stores_collection = db.get_collection("stores")
forecasts_collection = db.get_collection("forecasts")
# Time Constants
MIN_HOUR = 0
MAX_HOUR = 23

# Default Config Values (The fallback if JSON is missing)
DEFAULT_INTERVAL_HOURS = 24
DEFAULT_AVERAGE_DAYS = 7

STORES_COLLECTION = "stores"
FORECASTS_COLLECTION = "forecasts"
SALES_COLLECTION = "sales"
DB_NAME = "kfc_sales_forecast"

# --- Seed Data Constants ---
SEED_NUM_SALES = 500
SEED_MIN_QTY = 5
SEED_MAX_QTY = 50
SEED_MIN_HOUR = 10
SEED_MAX_HOUR = 23
SEED_DAYS_BACK = 7

PRODUCTS = ["Original Bucket", "Zinger Burger", "Twister Wrap", "Hot Wings"]

STORES = [
    {"store_id": "1", "name": "Tel Aviv Branch", "city": "Tel Aviv"},
    {"store_id": "2", "name": "Haifa Branch", "city": "Haifa"},
    {"store_id": "3", "name": "Jerusalem Branch", "city": "Jerusalem"}
]
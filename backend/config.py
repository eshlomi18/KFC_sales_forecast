import os
import json
from pydantic_settings import BaseSettings
from constants import DEFAULT_INTERVAL_HOURS, DEFAULT_AVERAGE_DAYS


class Settings(BaseSettings):
    # תשתית
    mongo_url: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")

    forecast_interval_hours: int = DEFAULT_INTERVAL_HOURS
    average_days_back: int = DEFAULT_AVERAGE_DAYS


settings = Settings()

# טעינת קובץ הקונפיגורציה
config_path = os.path.join(os.path.dirname(__file__), "config.json")
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        file_settings = json.load(f)
        # שימוש בקבועים גם ב-get!
        settings.forecast_interval_hours = file_settings.get("forecast_interval_hours", DEFAULT_INTERVAL_HOURS)
        settings.average_days_back = file_settings.get("average_days_back", DEFAULT_AVERAGE_DAYS)
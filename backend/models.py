from pydantic import BaseModel, Field, field_serializer
from datetime import datetime, timezone
from typing import List
from constants import MIN_HOUR, MAX_HOUR


class SalesForecastDB(BaseModel):
    store_id: str
    product_name: str
    hour: int = Field(..., ge=MIN_HOUR, le=MAX_HOUR)
    forecast_date: datetime
    predicted_sales: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Formats the raw database data for frontend presentation
class SalesForecastUI(SalesForecastDB):

    @field_serializer('forecast_date')
    def serialize_date(self, date_val: datetime, _info):
        return date_val.strftime('%Y-%m-%d')

    @field_serializer('hour')
    def serialize_hour(self, hour_val: int, _info):
        return f"{hour_val:02d}:00"


# ensures API response is serialized correctly
class ForecastResponse(BaseModel):
    forecasts: List[SalesForecastUI]
    total_count: int
    skip: int
    limit: int

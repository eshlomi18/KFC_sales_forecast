from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from constants import MIN_HOUR, MAX_HOUR

class Product(BaseModel):
    name: str
    price: float

class Store(BaseModel):
    name: str
    location: str
    products: List[Product] = []

class SalesForecast(BaseModel):
    store_id: str
    product_name: str
    hour: int = Field(..., ge=MIN_HOUR, le=MAX_HOUR)
    forecast_date: datetime
    predicted_sales: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
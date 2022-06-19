from datetime import datetime

from pydantic import BaseModel, Field
from custom_objectID import ObjID
from enum import Enum
from weather_service.schemas import WeatherSchema


class PaymentStatus(Enum):
    PAID = 'paid'
    UNPAID = 'unpaid'


class Point(BaseModel):
    longitude: float
    latitude: float


class TripSchema(BaseModel):
    id: ObjID = Field(alias='_id')
    bike_id: str
    user_id: str
    start_station_id: str
    finish_station_id: str
    start_time: datetime
    end_time: datetime
    travel_time: float
    price_bike: float
    total_amount: float
    points: list[Point]
    payment_status: PaymentStatus
    weather_begin: WeatherSchema
    weather_end: WeatherSchema

    class Config:
        json_encoders = {
            ObjID: lambda x: str(x),
            datetime: lambda x: x.strftime('%Y:%m:%d %H:%M')
        }

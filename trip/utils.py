import datetime
from typing import Optional

from bson import ObjectId
from fastapi import HTTPException, status

from trip.schemas import PaymentStatus
from configs import get_configs
from weather_service.weather_network_service import WeatherNetworkService


class PrepareDocumentService:

    @staticmethod
    async def prepare_finish_trip_document(station_id: str, end_time: datetime, travel_time: float,
                                           total_amount: float, weather: Optional[dict],
                                           points: list):
        return {
            'finish_station_id': station_id,
            'end_time': end_time,
            'travel_time': travel_time,
            'total_amount': round(total_amount, 2),
            'payment_status': PaymentStatus.PAID.value,
            'weather_end': weather,
            'points': points
        }

    @staticmethod
    async def prepare_start_trip_document(bike_id: str, bike: dict, user_id: str, weather: Optional[dict]):
        return {
            'bike_id': bike_id,
            'price_bike': bike['rent_price'],
            'total_amount': 0.0,
            'user_id': user_id,
            'start_station_id': bike['station_id'],
            'finish_station_id': None,
            'start_time': datetime.datetime.utcnow(),
            'end_time': None,
            'payment_status': PaymentStatus.UNPAID.value,
            'weather_begin': weather
        }


class CalculatesService:
    @staticmethod
    def calculate_datetime(start_time: datetime):
        end_time = datetime.datetime.utcnow()
        travel_time = (end_time - start_time).seconds
        return end_time, travel_time

    @staticmethod
    def calculate_total_amount(time_in_seconds: int, rent_price: float):
        return (time_in_seconds / 60) * rent_price


class CheckWeatherService:
    @staticmethod
    async def data(city_name: str, weather_service: WeatherNetworkService):
        params = {'q': city_name, 'units': 'metric', 'appid': get_configs().weather_api_key}
        if (weather := await weather_service.fetch_data(params=params)) is not None:
            weather = weather.dict()
        return weather

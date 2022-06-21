from abc import ABC, abstractmethod
from typing import Optional

from weather_service.schemas import WeatherSchema


class WeatherNetworkServiceInterface(ABC):

    @staticmethod
    @abstractmethod
    async def fetch_data(params: dict) -> Optional[WeatherSchema]:
        pass

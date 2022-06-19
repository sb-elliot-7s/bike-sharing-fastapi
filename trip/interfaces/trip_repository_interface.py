from abc import ABC, abstractmethod

from weather_service.network_service import WeatherNetworkService


class TripRepositoryInterface(ABC):
    @abstractmethod
    async def get_detail_trip(self, trip_id: str, user_id: str) -> None:
        pass

    @abstractmethod
    async def create_trip(self, bike_id: str, user_id: str, weather_service: WeatherNetworkService):
        pass

    @abstractmethod
    async def finish_trip(self, station_id: str, user_id: str, weather_service: WeatherNetworkService):
        pass

from trip.interfaces.trip_repository_interface import TripRepositoryInterface
from weather_service.weather_network_service import WeatherNetworkService


class TripService:

    def __init__(self, repository: TripRepositoryInterface):
        self.repository = repository

    async def create_trip(
            self, bike_id: str, user_id: str,
            weather_service: WeatherNetworkService
    ):
        return await self.repository.create_trip(
            bike_id=bike_id, user_id=user_id, weather_service=weather_service)

    async def finish_trip(
            self, station_id: str, user_id: str,
            weather_service: WeatherNetworkService
    ):
        return await self.repository \
            .finish_trip(station_id=station_id, user_id=user_id,
                         weather_service=weather_service)

    async def get_trip(self, trip_id: str, user_id: str):
        return await self.repository.get_detail_trip(
            trip_id=trip_id, user_id=user_id
        )

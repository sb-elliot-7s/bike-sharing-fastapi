from .interfaces.station_repository_interface import StationRepositoryInterface
from .schemas import CreateStationSchema, UpdateStationSchema


class StationService:
    def __init__(self, repository: StationRepositoryInterface):
        self._repository = repository

    async def create_station(self, station_data: CreateStationSchema):
        return await self._repository.create_station(**station_data.dict())

    async def get_detail_station(self, station_id: str):
        return await self._repository.get_detail_station(station_id=station_id)

    async def show_stations(self, city: str):
        return await self._repository.show_stations(city=city)

    async def update_station_info(self, station_id: str,
                                  station_data: UpdateStationSchema):
        return await self._repository.update_station_info(
            station_id=station_id,
            station_data=station_data.dict(exclude_none=True)
        )

    async def delete_station(self, station_id: str):
        return await self._repository.delete_station(station_id=station_id)

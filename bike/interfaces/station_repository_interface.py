from abc import ABC, abstractmethod


class StationRepositoryInterface(ABC):

    @abstractmethod
    async def create_station(
            self, station_name: str, maximum_number_of_bicycles: int,
            address: dict):
        pass

    @abstractmethod
    async def show_stations(self, city: str): pass

    @abstractmethod
    async def get_detail_station(self, station_id: str): pass

    @abstractmethod
    async def update_station_info(self, station_id: str, station_data: dict):
        pass

    @abstractmethod
    async def delete_station(self, station_id: str): pass

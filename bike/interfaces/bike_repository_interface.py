from abc import ABC, abstractmethod
from typing import Optional
from ..schemas import CreateBikeSchema


class BikeRepositoryInterface(ABC):

    @abstractmethod
    async def create_bike(self, bike_serial: str, station_id: str, brand: str,
                          model: str, color: str, rent_price: float,
                          bike_manufacturer: Optional[str] = None,
                          description: Optional[str] = None):
        pass

    @abstractmethod
    async def get_bike(self, bike_id: str): pass

    @abstractmethod
    async def update_info_bike(self, bike_id: str, update_bike_data: dict): pass

    @abstractmethod
    async def delete_bike(self, bike_id: str): pass

    @abstractmethod
    async def add_many_bikes_for_station(self, station_id: str, _bikes: list[CreateBikeSchema]):
        pass

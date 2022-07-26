from abc import ABC, abstractmethod


class GeoServiceInterface(ABC):
    @abstractmethod
    async def get_longitude_and_latitude(
            self, country: str, city: str, street: str, house: str):
        pass

    @abstractmethod
    async def get_address(self, latitude: float, longitude: float):
        pass

from .interfaces.geo_service import GeoServiceInterface
from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter


class GeoService(GeoServiceInterface):
    def __init__(self):
        self._nominatim = Nominatim(user_agent='bike', adapter_factory=AioHTTPAdapter)

    async def get_longitude_and_latitude(self, country: str, city: str,
                                         street: str, house: str):
        async with self._nominatim as geo:
            address = {
                'street': f'{house} {street}',
                'city': city,
                'country': country
            }
            location = await geo.geocode(address)
            return location.latitude, location.longitude

    async def get_address(self, latitude: float, longitude: float):
        async with self._nominatim as geo:
            query = f'{latitude}, {longitude}'
            location = geo.reverse(query=query, language='ru_RU')
            return location.address

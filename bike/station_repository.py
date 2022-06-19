import datetime

from bson import ObjectId
from fastapi import HTTPException, status

from .interfaces.station_repository_interface import StationRepositoryInterface


class StationRepository(StationRepositoryInterface):
    def __init__(self, station_collection):
        self._station_collection = station_collection

    async def _get_station(self, station_id: str):
        if not (station := await self._station_collection.find_one(filter={'_id': ObjectId(station_id)})):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Station not found')
        return station

    async def create_station(self, station_name: str, maximum_number_of_bicycles: int, address: dict):
        document = {
            'station_name': station_name,
            'maximum_number_of_bicycles': maximum_number_of_bicycles,
            'address': address,
            'available_count_of_bicycles': 0,
            'bicycles': [],
            'time_created': datetime.datetime.utcnow(),
        }
        result = await self._station_collection.insert_one(document=document)
        return await self._get_station(station_id=result.inserted_id)

    async def show_stations(self, city: str):
        cursor = self._station_collection.find(filter={'address.city': city})
        return [station async for station in cursor]

    # async def find_nearest_station(self): pass

    async def get_detail_station(self, station_id: str):
        return await self._get_station(station_id=station_id)

    async def update_station_info(self, station_id: str, station_data: dict):
        if max_num := station_data.get('maximum_number_of_bicycles'):
            station_data.update({'available_count_of_bicycles': max_num})
        station_data.update({'time_updated': datetime.datetime.utcnow()})

        if 'address' in station_data and (address := station_data.pop('address')):
            station_data.update({f'address.{key}': value for key, value in address.items()})
        attrs = {
            'filter': {'_id': ObjectId(station_id)},
            'update': {'$set': station_data},
            'return_document': True
        }
        return await self._station_collection.find_one_and_update(**attrs)

    async def delete_station(self, station_id: str):
        station = await self._get_station(station_id=station_id)
        result = await self._station_collection.delete_one(filter={'_id': ObjectId(station['_id'])})
        return False if not result.deleted_count else True

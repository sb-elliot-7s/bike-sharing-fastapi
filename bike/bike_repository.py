import datetime
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
from .constants import response_exceptions
from .interfaces.bike_repository_interface import BikeRepositoryInterface


class BikeRepository(BikeRepositoryInterface):

    def __init__(self, bike_collection, station_collection):
        self._station_collection = station_collection
        self._bike_collection = bike_collection

    async def _get_detail_bike(self, bike_id: str):
        if not (bike := await self._bike_collection.find_one(filter={'_id': ObjectId(bike_id)})):
            raise HTTPException(**response_exceptions.get('bike_not_found'))
        return bike

    async def get_bike(self, bike_id: str):
        return await self._get_detail_bike(bike_id=bike_id)

    async def update_info_bike(self, bike_id: str, update_bike_data: dict):
        attrs = {
            'filter': {'_id': ObjectId(bike_id)},
            'update': {'$set': update_bike_data},
            'return_document': True
        }
        return await self._bike_collection.find_one_and_update(**attrs)

    async def delete_bike(self, bike_id: str):
        bike = await self._get_detail_bike(bike_id=bike_id)
        result = await self._bike_collection.delete_one(filter={'_id': ObjectId(bike['_id'])})
        return False if not result.deleted_count else True

    @staticmethod
    async def _prepare_document(bike_manufacturer, bike_serial, brand, color, description, model,
                                rent_price, station_id):
        return {
            'bike_serial': bike_serial,
            'station_id': station_id,
            'brand': brand,
            'model': model,
            'color': color,
            'bike_manufacturer': bike_manufacturer,
            'description': description,
            'rent_price': rent_price,
            'created': datetime.datetime.utcnow()
        }

    async def create_bike(self, bike_serial: str, station_id: str, brand: str, model: str,
                          color: str, rent_price: float, bike_manufacturer: Optional[str] = None,
                          description: Optional[str] = None):
        document = await self._prepare_document(bike_manufacturer, bike_serial, brand, color, description,
                                                model, rent_price, station_id)
        result = await self._bike_collection.insert_one(document=document)
        bike = await self._get_detail_bike(bike_id=result.inserted_id)
        station = await self._station_collection.find_one({'_id': ObjectId(station_id)})
        if not station['available_count_of_bicycles'] > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'There are {station["maximum_number_of_bicycles"]} '
                                       f'bike places available at the station. Everyone is busy')
        updated_data = {
            'filter': {'_id': ObjectId(station_id)},
            'update': {'$inc': {'available_count_of_bicycles': -1}, '$push': {'bicycles': bike}}
        }
        await self._station_collection.update_one(**updated_data)
        return bike

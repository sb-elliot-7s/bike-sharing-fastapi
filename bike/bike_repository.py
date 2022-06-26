import datetime
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status

from .bike_utils import BikeUtils
from .constants import response_exceptions
from .interfaces.bike_repository_interface import BikeRepositoryInterface
from .schemas import CreateBikeSchema, BikeSchema


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
        data = await BikeUtils().get_update_info_bike(bike_data=update_bike_data, bike_id=bike_id)
        return await self._bike_collection.find_one_and_update(**data)

    async def delete_bike(self, bike_id: str):
        bike = await self._get_detail_bike(bike_id=bike_id)
        result = await self._bike_collection.delete_one(filter={'_id': ObjectId(bike['_id'])})
        return False if not result.deleted_count else True

    async def _check_available_count_of_bikes(self, station_id: str):
        station = await self._station_collection.find_one({'_id': ObjectId(station_id)})
        station_available_count_of_bikes = station['available_count_of_bicycles']
        if not station_available_count_of_bikes > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'There are {station["maximum_number_of_bicycles"]} '
                                       f'bike places available at the station. Everyone is busy')
        return station, station_available_count_of_bikes

    @staticmethod
    def _get_updated_data(station_id: str, _updated_filter: dict):
        return {'filter': {'_id': ObjectId(station_id)}, 'update': _updated_filter}

    async def create_bike(self, bike_serial: str, station_id: str, brand: str, model: str,
                          color: str, rent_price: float, bike_manufacturer: Optional[str] = None,
                          description: Optional[str] = None):
        document = await BikeUtils() \
            .prepare_document(bike_manufacturer=bike_manufacturer, bike_serial=bike_serial, brand=brand,
                              color=color, description=description, model=model, rent_price=rent_price,
                              station_id=station_id)
        result = await self._bike_collection.insert_one(document=document)
        bike = await self._get_detail_bike(bike_id=result.inserted_id)
        station = await self._station_collection.find_one({'_id': ObjectId(station_id)})
        if len(station['bicycles']) < station['maximum_number_of_bicycles']:
            _filter = {'$inc': {'available_count_of_bicycles': 1}, '$push': {'bicycles': bike}}
            updated_data = self._get_updated_data(station_id=station_id, _updated_filter=_filter)
            await self._station_collection.update_one(**updated_data)
            return bike
        return False

    async def add_many_bikes_for_station(self, station_id: str, _bikes: list[CreateBikeSchema]):
        data = [dict(doc.dict(exclude_none=True), created=datetime.datetime.utcnow()) for doc in _bikes]
        result = await self._bike_collection.insert_many(data)
        station = await self._station_collection.find_one({'_id': ObjectId(station_id)})
        bikes = [await self._get_detail_bike(bike_id=bike_id) for bike_id in result.inserted_ids]
        add_count_of_bikes = len(bikes)
        max_count = station['maximum_number_of_bicycles']
        available_count_of_bicycles = station['available_count_of_bicycles']
        dif = (max_count - available_count_of_bicycles)
        cnt = add_count_of_bikes if add_count_of_bikes < dif else dif
        if available_count_of_bicycles < max_count:
            updated_data = self._get_updated_data(
                station_id=station_id,
                _updated_filter={'$inc': {'available_count_of_bicycles': cnt},
                                 '$push': {'bicycles': {'$each': bikes[:cnt]}}})
            await self._station_collection.update_one(**updated_data)
        return {
            'max_count': max_count,
            'available_count': available_count_of_bicycles,
            'added': cnt,
            'not added': add_count_of_bikes - cnt,
            'bikes_added': [BikeSchema(**bike) for bike in bikes[:cnt]]
        }

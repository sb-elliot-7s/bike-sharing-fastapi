import datetime
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException
from bike.constants import response_exceptions
from bike.schemas import CreateBikeSchema
from .bike_mixins import BikeRepositoryMixin, BikePrepareDocumentMixin, \
    CalculateCountOfBikesOnTheStationMixin


class BikeStationRepository(
    BikePrepareDocumentMixin, CalculateCountOfBikesOnTheStationMixin
):
    @staticmethod
    async def __create_bikes_and_return_ids(
            bike_coll, bikes: list[CreateBikeSchema]
    ):
        data = [dict(doc.dict(exclude_none=True),
                     created=datetime.datetime.utcnow()) for doc in bikes]
        result = await bike_coll.insert_many(data)
        return result.inserted_ids

    @staticmethod
    async def __find_station(station_coll, station_id: str):
        if not (station := await station_coll.find_one(
                {'_id': ObjectId(station_id)})):
            raise HTTPException(**response_exceptions.get('station_not_found'))
        return station

    @staticmethod
    async def update_station(station_coll, station_id: str, bike_count: int,
                             bike_objects: dict):
        _filter = {
            '$inc': {
                'available_count_of_bicycles': bike_count
            },
            '$push': {
                'bicycles': bike_objects
            }
        }
        await station_coll.update_one(
            **BikeRepositoryMixin().get_updated_data(station_id, _filter))

    async def check_count_of_bikes_and_update_station(self, station_coll,
                                                      station_id: str,
                                                      bike_count: int,
                                                      bike: dict):
        station = await self.__find_station(station_id=station_id,
                                            station_coll=station_coll)
        if len(station['bicycles']) < station['maximum_number_of_bicycles']:
            await self. \
                update_station(station_id=station_id, bike_count=bike_count,
                               bike_objects=bike,
                               station_coll=station_coll)
            return True
        return False

    async def response_data_station(self, station_id: str, bikes: list,
                                    station_coll):
        station = await self.__find_station(station_id=station_id,
                                            station_coll=station_coll)
        results_of_counts = await self.calculate_bikes_on_the_station(
            station=station, bikes=bikes)
        available_count_of_bicycles, max_count, cnt, add_count_of_bikes = \
            results_of_counts
        if available_count_of_bicycles < max_count:
            await self.update_station(
                station_coll, station_id, cnt, {'$each': bikes[:cnt]}
            )
        return await self.get_response_data(
            max_count=max_count, count=cnt, bikes=bikes,
            add_count_of_bikes=add_count_of_bikes,
            available_count_of_bicycles=available_count_of_bicycles)

    @staticmethod
    async def get_detail_bike(bike_coll, bike_id: str):
        if not (
                bike := await bike_coll.find_one(
                    filter={'_id': ObjectId(bike_id)})):
            raise HTTPException(**response_exceptions.get('bike_not_found'))
        return bike

    async def create_and_return_bike(self, bike_coll, bike_serial: str,
                                     brand: str, color: Optional[str],
                                     model: str, rent_price: Optional[float],
                                     station_id: str,
                                     bike_manufacturer: Optional[str],
                                     description: Optional[str]):
        document = await self.prepare_document(
            bike_manufacturer=bike_manufacturer, bike_serial=bike_serial,
            brand=brand, color=color,
            description=description, model=model, rent_price=rent_price,
            station_id=station_id)
        result = await bike_coll.insert_one(document=document)
        return await self.get_detail_bike(bike_id=result.inserted_id,
                                          bike_coll=bike_coll)

    async def get_bikes(self, bike_coll, bikes: list[CreateBikeSchema]):
        ids = await self.__create_bikes_and_return_ids(bike_coll=bike_coll,
                                                       bikes=bikes)
        return [
            await self.get_detail_bike(bike_id=bike_id, bike_coll=bike_coll)
            for bike_id in ids
        ]

import datetime
from typing import Optional

from bson import ObjectId

from bike.schemas import BikeSchema


class BikeRepositoryMixin:
    @staticmethod
    def get_updated_data(station_id: str, _updated_filter: dict):
        return {'filter': {'_id': ObjectId(station_id)},
                'update': _updated_filter}


class BikePrepareDocumentMixin:
    @staticmethod
    async def prepare_document(bike_serial: str, brand: str, color: str,
                               model: str, station_id: str,
                               rent_price: Optional[float],
                               bike_manufacturer: Optional[str] = None,
                               description: Optional[str] = None):
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

    @staticmethod
    async def get_update_info_bike_data(bike_data: dict, bike_id: str):
        return {
            'filter': {'_id': ObjectId(bike_id)},
            'update': {'$set': bike_data},
            'return_document': True
        }

    @staticmethod
    async def get_response_data(max_count, available_count_of_bicycles,
                                add_count_of_bikes, count, bikes):
        return {
            'max_count': max_count,
            'available_count': available_count_of_bicycles,
            'added': count,
            'not added': add_count_of_bikes - count,
            'bikes_added': [BikeSchema(**bike) for bike in bikes[:count]]
        }


class CalculateCountOfBikesOnTheStationMixin:
    @staticmethod
    async def calculate_bikes_on_the_station(station: dict, bikes: list):
        add_count_of_bikes = len(bikes)
        max_count = station['maximum_number_of_bicycles']
        available_count_of_bicycles = station['available_count_of_bicycles']
        dif = (max_count - available_count_of_bicycles)
        cnt = add_count_of_bikes if add_count_of_bikes < dif else dif
        return available_count_of_bicycles, max_count, cnt, add_count_of_bikes

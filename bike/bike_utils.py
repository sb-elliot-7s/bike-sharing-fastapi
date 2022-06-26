import datetime
from typing import Optional

from bson import ObjectId


class BikeUtils:
    @staticmethod
    async def prepare_document(bike_serial: str, brand: str, color: str, model: str, rent_price: float,
                               station_id: str, bike_manufacturer: Optional[str] = None,
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
    async def get_update_info_bike(bike_data: dict, bike_id: str):
        return {
            'filter': {'_id': ObjectId(bike_id)},
            'update': {'$set': bike_data},
            'return_document': True
        }

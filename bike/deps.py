from fastapi import Depends

from database import database
from .bike_repository import BikeRepository
from .station_repository import StationRepository

bike_collection = database.bike
station_collection = database.station


async def get_bike_collection(): yield bike_collection


async def get_station_collection(): yield station_collection


async def get_bike_service(_bike_collection=Depends(get_bike_collection),
                           _station_collection=Depends(get_station_collection)):
    yield {
        'repository': BikeRepository(
            bike_collection=_bike_collection, station_collection=station_collection
        )
    }


async def get_station_service(_station_collection=Depends(get_station_collection)):
    yield {
        'repository': StationRepository(station_collection=_station_collection)
    }

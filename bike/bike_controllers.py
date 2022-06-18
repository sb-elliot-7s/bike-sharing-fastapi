from fastapi import APIRouter, Depends
from .repositories import BikeRepository
from .services import BikeService
from .deps import get_bike_collection

bike_router = APIRouter(prefix='/bike', tags=['bike'])
station_router = APIRouter(prefix='/station', tags=['station'])


@station_router.post('/')
async def create_station():
    pass


@station_router.get('/')
async def get_all_station():
    pass


@station_router.get('/near')
async def find_nearest_station():
    pass


@station_router.get('/{station_id}')
async def get_detail_station():
    pass


@station_router.patch('/{station_id}')
async def update_station_info(station_id: str):
    pass


@bike_router.post('/')
async def create_bike(bike_collection=Depends(get_bike_collection)):
    await BikeService(repository=BikeRepository(bike_collection=bike_collection)).create_bike()


@bike_router.get('/{bike_id}')
async def get_bike(bike_id: str, bike_collection=Depends(get_bike_collection)):
    pass


@bike_router.patch('/{bike_id}')
async def update_info_bike(bike_id: str):
    pass


@bike_router.delete('/{bike_id}')
async def delete_bike(bike_id: str):
    pass

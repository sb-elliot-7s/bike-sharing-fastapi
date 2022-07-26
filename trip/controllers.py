from fastapi import APIRouter, Depends, status
from .deps import get_trip_collection
from .services import TripService
from .repositories import TripRepository
from bike.deps import get_bike_collection, get_station_collection
from permissions import Permission
from account.token_service import TokenService
from weather_service.weather_network_service import WeatherNetworkService
from .schemas import TripSchema

trip_router = APIRouter(prefix='/trip', tags=['trip'])


async def get_trip_services(trip_collection=Depends(get_trip_collection),
                            bike_collection=Depends(get_bike_collection),
                            station_collection=Depends(get_station_collection)):
    yield {
        'repository': TripRepository(
            trip_collection=trip_collection, bike_collection=bike_collection,
            station_collection=station_collection
        )
    }


@trip_router.get('/{trip_id}', status_code=status.HTTP_200_OK,
                 response_model=TripSchema, response_model_by_alias=False)
async def get_trip(trip_id: str, services=Depends(get_trip_services),
                   user=Depends(Permission(token_service=TokenService()))):
    return await TripService(**services) \
        .get_trip(trip_id=trip_id, user_id=user.id)


@trip_router.post('/start/{bike_id}', status_code=status.HTTP_201_CREATED)
async def create_trip(bike_id: str, services=Depends(get_trip_services),
                      user=Depends(Permission(token_service=TokenService()))):
    await TripService(**services) \
        .create_trip(user_id=user.id, bike_id=bike_id,
                     weather_service=WeatherNetworkService())


@trip_router.post('/finish/{station_id}')
async def finish_trip(station_id: str, services=Depends(get_trip_services),
                      user=Depends(Permission(token_service=TokenService()))):
    await TripService(**services) \
        .finish_trip(station_id=station_id, user_id=user.id,
                     weather_service=WeatherNetworkService())

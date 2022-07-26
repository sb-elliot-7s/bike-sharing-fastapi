from fastapi import APIRouter, Depends, HTTPException, responses, status
from .schemas import CreateStationSchema, UpdateStationSchema
from .station_service import StationService
from .constants import station_response_data
from .deps import get_station_service
from permissions import Permission
from account.token_service import TokenService

station_router = APIRouter(prefix='/station', tags=['station'])


@station_router.post('/', **station_response_data.get('create'))
async def create_station(station_data: CreateStationSchema,
                         services=Depends(get_station_service),
                         admin_user=Depends(
                             Permission(token_service=TokenService())
                             .get_admin_user)):
    return await StationService(**services) \
        .create_station(station_data=station_data)


# find all stations in the city
@station_router.get('/', **station_response_data.get('show_all_stations'))
async def show_all_stations_in_the_city(
        city: str, services=Depends(get_station_service)
):
    return await StationService(**services).show_stations(city=city)


# show specific station
@station_router.get('/{station_id}',
                    **station_response_data.get('detail_station'))
async def get_detail_station(
        station_id: str, services=Depends(get_station_service)
):
    return await StationService(**services) \
        .get_detail_station(station_id=station_id)


@station_router.patch('/{station_id}',
                      **station_response_data.get('detail_station'))
async def update_station_info(station_id: str,
                              station_data: UpdateStationSchema,
                              services=Depends(get_station_service),
                              admin_user=Depends(
                                  Permission(token_service=TokenService())
                                  .get_admin_user)):
    return await StationService(**services) \
        .update_station_info(station_id=station_id, station_data=station_data)


@station_router.delete('/{station_id}',
                       **station_response_data.get('delete_station'))
async def delete_station(station_id: str, services=Depends(get_station_service),
                         admin_user=Depends(
                             Permission(token_service=TokenService())
                             .get_admin_user)):
    if not (_ := await StationService(**services).delete_station(
            station_id=station_id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Station not deleted')
    return responses.JSONResponse({'detail': 'Station has been deleted'})

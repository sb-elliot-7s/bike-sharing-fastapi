from fastapi import APIRouter, Depends, HTTPException, responses, status
from .bike_service import BikeService
from .schemas import CreateBikeSchema, UpdateBikeSchema
from .deps import get_bike_service
from .constants import response_exceptions, bike_response_data

from account.token_service import TokenService
from permissions import Permission

bike_router = APIRouter(prefix='/bike', tags=['bike'])


@bike_router.post('/', **bike_response_data.get('create'))
async def create_bike(bike_data: CreateBikeSchema,
                      services=Depends(get_bike_service),
                      admin_user=Depends(
                          Permission(token_service=TokenService())
                          .get_admin_user)
                      ):
    if not (result := await BikeService(**services)
            .create_bike(bike_data=bike_data, user=admin_user)):
        return responses.JSONResponse(
            content={'detail': 'Failed to add bike to station'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return result


@bike_router.get('/{bike_id}', **bike_response_data.get('detail'))
async def get_bike(bike_id: str, services=Depends(get_bike_service)):
    return await BikeService(**services).get_bike(bike_id=bike_id)


@bike_router.patch('/{bike_id}', **bike_response_data.get('detail'))
async def update_info_bike(bike_id: str, bike_data: UpdateBikeSchema,
                           services=Depends(get_bike_service),
                           admin_user=Depends(
                               Permission(token_service=TokenService())
                               .get_admin_user)
                           ):
    return await BikeService(**services).update_info_bike(
        bike_id=bike_id, updated_data=bike_data, user=admin_user
    )


@bike_router.delete('/{bike_id}', **bike_response_data.get('delete'))
async def delete_bike(bike_id: str, services=Depends(get_bike_service),
                      admin_user=Depends(
                          Permission(token_service=TokenService())
                          .get_admin_user)
                      ):
    if not (_ := await BikeService(**services)
            .delete_bike(bike_id=bike_id, user=admin_user)):
        raise HTTPException(**response_exceptions.get('bike_bad_request'))
    return responses.JSONResponse({'detail': 'Bike has been deleted'})


@bike_router.post('/create/all')
async def add_many_bikes_for_station(
        station_id: str, list_of_bikes: list[CreateBikeSchema],
        services=Depends(get_bike_service),
        admin_user=Depends(
            Permission(token_service=TokenService()).get_admin_user)):
    return await BikeService(**services).add_many_bikes_for_station(
        station_id=station_id, list_of_bikes=list_of_bikes, user=admin_user
    )

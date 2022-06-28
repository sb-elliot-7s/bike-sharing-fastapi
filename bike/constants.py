from typing import Union

from fastapi import status
from .schemas import BikeSchema, StationSchema

response_exceptions = {
    'bike_bad_request': {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'detail': 'Bike not deleted'
    },
    'bike_not_found': {
        'status_code': status.HTTP_404_NOT_FOUND,
        'detail': 'Bike not found'
    },
    'station_not_found': {
        'status_code': status.HTTP_404_NOT_FOUND,
        'detail': 'Station not found'
    }
}

bike_response_data = {
    'create': {
        'status_code': status.HTTP_201_CREATED,
        'response_model': Union[BikeSchema, dict],
        'response_model_by_alias': False
    },
    'detail': {
        'status_code': status.HTTP_200_OK,
        'response_model': BikeSchema,
        'response_model_by_alias': False
    },
    'delete': {
        'status_code': status.HTTP_204_NO_CONTENT
    }
}

station_response_data = {
    'create': {
        'status_code': status.HTTP_201_CREATED,
        'response_model': StationSchema,
        'response_model_by_alias': False
    },
    'show_all_stations': {
        'status_code': status.HTTP_200_OK,
        'response_model': list[StationSchema],
        'response_model_by_alias': False
    },
    'detail_station': {
        'status_code': status.HTTP_200_OK,
        'response_model': StationSchema,
        'response_model_by_alias': False
    },
    'delete_station': {
        'status_code': status.HTTP_204_NO_CONTENT,
        'response_model_by_alias': False
    }
}

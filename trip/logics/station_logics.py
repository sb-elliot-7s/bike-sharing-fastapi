from bson import ObjectId
from fastapi import HTTPException, status


class CommonStationService:
    @staticmethod
    async def get_and_update_station(station_collection, station_id: str, _update: dict):
        if (station := await station_collection.find_one_and_update(
                return_document=True, filter={'_id': ObjectId(station_id)}, update=_update
        )) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Station not found')
        return station

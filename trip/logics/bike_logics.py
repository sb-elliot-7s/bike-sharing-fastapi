from bson import ObjectId
from fastapi import HTTPException, status


class CommonBikeService:
    @staticmethod
    async def bike_update(bike_collection, bike_id: str, station_id: str):
        if (bike := await bike_collection.find_one_and_update(
                {'_id': ObjectId(bike_id)}, {'$set': {'station_id': station_id}}, return_document=True
        )) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bike not found')
        return bike

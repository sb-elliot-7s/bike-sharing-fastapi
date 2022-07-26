from bson import ObjectId
from .bike_station_utils import BikeStationRepository
from .interfaces.bike_repository_interface import BikeRepositoryInterface
from .schemas import CreateBikeSchema


class BikeRepository(BikeStationRepository, BikeRepositoryInterface):

    def __init__(self, bike_collection, station_collection):
        self._station_collection = station_collection
        self._bike_collection = bike_collection

    async def get_bike(self, bike_id: str):
        return await self.get_detail_bike(
            bike_id=bike_id, bike_coll=self._bike_collection
        )

    async def update_info_bike(
            self, user, bike_id: str, update_bike_data: dict
    ):
        data = await self.get_update_info_bike_data(
            user_id=user.id,
            bike_data=update_bike_data,
            bike_id=bike_id
        )
        return await self._bike_collection.find_one_and_update(**data)

    async def delete_bike(self, user, bike_id: str):
        bike = await self.get_detail_bike(
            bike_id=bike_id, bike_coll=self._bike_collection
        )
        result = await self._bike_collection.delete_one(
            filter={
                '_id': ObjectId(bike['_id']),
                'account_id': user.id
            }
        )
        return False if not result.deleted_count else True

    async def create_bike(self, user, bike_data: CreateBikeSchema):
        bike = await self.create_and_return_bike(
            user_id=user.id,
            bike_coll=self._bike_collection,
            **bike_data.dict(exclude_none=True)
        )
        return bike if await self.check_count_of_bikes_and_update_station(
            station_id=bike_data.station_id, bike_count=1, bike=bike,
            station_coll=self._station_collection) else False

    async def add_many_bikes_for_station(
            self, user, station_id: str, _bikes: list[CreateBikeSchema]
    ):
        bikes = await self.get_bikes(
            bike_coll=self._bike_collection, bikes=_bikes, user_id=user.id
        )
        return await self.response_data_station(
            station_id=station_id,
            bikes=bikes,
            station_coll=self._station_collection
        )

from .interfaces.bike_repository_interface import BikeRepositoryInterface
from .schemas import CreateBikeSchema, UpdateBikeSchema


class BikeService:
    def __init__(self, repository: BikeRepositoryInterface):
        self.repository = repository

    async def create_bike(self, bike_data: CreateBikeSchema):
        return await self.repository.create_bike(**bike_data.dict(exclude_none=True))

    async def get_bike(self, bike_id: str): return await self.repository.get_bike(bike_id=bike_id)

    async def update_info_bike(self, bike_id: str, updated_data: UpdateBikeSchema):
        return await self.repository \
            .update_info_bike(bike_id=bike_id, update_bike_data=updated_data.dict(exclude_none=True))

    async def delete_bike(self, bike_id: str): return await self.repository.delete_bike(bike_id=bike_id)

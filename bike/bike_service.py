class BikeService:
    def __init__(self, repository):
        self.repository = repository

    async def create_bike(self):
        await self.repository.create_bike()
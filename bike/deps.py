from database import database

bike_collection = database.bike


async def get_bike_collection(): yield bike_collection

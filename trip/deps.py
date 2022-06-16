from database import database

trip_collection = database.trip


async def get_trip_collection(): yield trip_collection

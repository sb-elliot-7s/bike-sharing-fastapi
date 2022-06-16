from database import database

address_collection = database.address


async def get_address_collection(): yield address_collection

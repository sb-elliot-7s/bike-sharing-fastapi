from database import database

payment_collection = database.payment


async def get_payment_collection():
    yield payment_collection

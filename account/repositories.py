import datetime
from typing import Optional

from .interfaces.repositories import AccountRepositoryInterface


class AccountRepository(AccountRepositoryInterface):
    def __init__(self, account_collection):
        self._account_collection = account_collection

    async def save_user(self, username: str, password: str, email: Optional[str]):
        document = {
            'username': username,
            'email': email,
            'password': password,
            'date_created': datetime.datetime.utcnow()
        }
        result = await self._account_collection.insert_one(document=document)
        return await self._account_collection.find_one({'_id': result.inserted_id})

    async def get_user_by(self, username: str):
        return await self._account_collection.find_one(filter={'username': username})

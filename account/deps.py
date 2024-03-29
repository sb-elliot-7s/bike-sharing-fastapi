from fastapi import Depends
from passlib.context import CryptContext

from account.password_service import PasswordService
from account.repositories import AccountRepository
from account.token_service import TokenService
from database import database

account_collection = database.account


async def get_account_collection(): yield account_collection


async def get_account_service(
        _account_collection=Depends(get_account_collection)
):
    yield {
        'token_service': TokenService(),
        'password_service': PasswordService(
            context=CryptContext(schemes=['bcrypt'],
                                 deprecated='auto')),
        'repository': AccountRepository(account_collection=_account_collection)
    }

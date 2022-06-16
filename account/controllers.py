from fastapi import APIRouter, Depends, status

from .schemas import CreateAccountSchema, AccountSchema, Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .deps import get_account_collection, get_account_service
from .services import AccountService

account_router = APIRouter(prefix='/account', tags=['account'])

response_data = {
    'registration': {
        'status_code': status.HTTP_201_CREATED,
        'response_model': AccountSchema
    }, 'login': {
        'status_code': status.HTTP_200_OK,
        'response_model': Token,
    },
}


@account_router.post('/registration', **response_data.get('registration'))
async def registration(user_data: CreateAccountSchema, service_data=Depends(get_account_service)):
    return await AccountService(**service_data).registration(user_data=user_data)


@account_router.post('/login', **response_data.get('login'))
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service_data=Depends(get_account_service)):
    return await AccountService(**service_data) \
        .login(username=form_data.username, password=form_data.password)

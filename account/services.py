from fastapi import HTTPException, status

from .interfaces.repositories import AccountRepositoryInterface
from .schemas import CreateAccountSchema
from .interfaces.token_service_interface import TokenServiceInterface
from .interfaces.password_interface import PasswordServiceInterface
from .constants import TokenType
from configs import get_configs


class AccountService:
    def __init__(self, repository: AccountRepositoryInterface,
                 token_service: TokenServiceInterface,
                 password_service: PasswordServiceInterface):
        self._password_service = password_service
        self._token_service = token_service
        self._repository = repository
        self._settings = get_configs()

    async def _create_token_data(
            self, username: str, token_type: TokenType, exp_time: int):
        return await self._token_service.encode_token(
            username=username, token_type=token_type,
            secret_key=self._settings.api_key,
            algorithm=self._settings.algorithm, exp_time=exp_time)

    async def _authenticate(self, username: str, password: str):
        if not (user := await self._repository.get_user_by(username=username)) \
                or not await self._password_service \
                .verify_passwords(plain_password=password,
                                  hashed_password=user['password']):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Incorrect username or password')
        return user

    async def login(self, username: str, password: str):
        user = await self._authenticate(username=username, password=password)
        access_token = await self._create_token_data(
            username=user['username'], token_type=TokenType.ACCESS_TOKEN,
            exp_time=self._settings.exp_time)
        refresh_token = await self._create_token_data(
            username=user['username'], token_type=TokenType.REFRESH_TOKEN,
            exp_time=10)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    async def registration(self, user_data: CreateAccountSchema):
        if await self._repository.get_user_by(username=user_data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='User with this username exists')
        hashed_password = await self._password_service.hashed_password(
            plain_password=user_data.password)
        data_without_password = user_data.dict(exclude={'password'})
        return await self._repository.save_user(password=hashed_password,
                                                **data_without_password)

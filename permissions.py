from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from account.interfaces.token_service_interface import TokenServiceInterface
from account.deps import get_account_collection
from account.schemas import AccountSchema
from configs import get_configs


class Permission:
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='auth/login')

    def __init__(self, token_service: TokenServiceInterface):
        self._token_service = token_service
        self._secret_key = get_configs().api_key
        self._algorithm = get_configs().algorithm

    async def _decode_token(self, token: str) -> str:
        payload: dict = await self._token_service.decode_access_token(
            access_token=token,
            secret_key=self._secret_key,
            algorithm=self._algorithm
        )
        if not (username := payload.get('sub')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=''
            )
        return username

    @staticmethod
    async def _find_user(_filter: dict, account_collection):
        if (user := await account_collection.find_one(filter=_filter)) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User not found or user is not admin')
        return user

    async def __call__(self, account_collection=Depends(get_account_collection),
                       token: str = Depends(OAUTH2_SCHEME)):
        username = await self._decode_token(token=token)
        user = await self._find_user(
            account_collection=account_collection,
            _filter={'username': username}
        )
        return AccountSchema(**user)

    async def get_admin_user(
            self, account_collection=Depends(get_account_collection),
            token: str = Depends(OAUTH2_SCHEME)
    ):
        username = await self._decode_token(token=token)
        user = await self._find_user(
            account_collection=account_collection,
            _filter={'username': username, 'is_admin': True}
        )
        return AccountSchema(**user)

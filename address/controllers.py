from fastapi import APIRouter

address_router = APIRouter(prefix='/address', tags=['address'])


@address_router.get('/')
async def get_address_location():
    pass

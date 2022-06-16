from fastapi import APIRouter, Depends, status

bike_router = APIRouter(prefix='/bike', tags=['bike'])

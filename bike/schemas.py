from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from custom_objectID import ObjID


class CreateAddressSchema(BaseModel):
    country: Optional[str]
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]


class AddressSchema(CreateAddressSchema):
    latitude: Optional[float]
    longitude: Optional[float]


class UpdateBikeSchema(BaseModel):
    color: Optional[str]
    rent_price: Optional[float]
    description: Optional[str]


class CreateBikeSchema(UpdateBikeSchema):
    bike_serial: str
    station_id: str
    brand: str
    model: str
    bike_manufacturer: Optional[str]


class BikeSchema(CreateBikeSchema):
    id: ObjID = Field(alias='_id')
    created: datetime
    updated: Optional[datetime]

    class Config:
        json_encoders = {
            ObjID: lambda x: str(x)
        }


class CreateStationSchema(BaseModel):
    station_name: str
    maximum_number_of_bicycles: int = 1
    address: CreateAddressSchema


class UpdateStationSchema(BaseModel):
    station_name: Optional[str]
    maximum_number_of_bicycles: Optional[int]
    address: Optional[CreateAddressSchema]


class StationSchema(CreateStationSchema):
    id: ObjID = Field(alias='_id')
    bicycles: list[BikeSchema]
    available_count_of_bicycles: int
    time_created: datetime
    time_updated: Optional[datetime]
    address: AddressSchema

    class Config:
        json_encoders = {
            ObjID: lambda x: str(x),
            datetime: lambda x: x.strftime('%Y:%m:%d %H:%M')
        }

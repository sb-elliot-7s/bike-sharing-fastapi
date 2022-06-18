from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from custom_objectID import ObjID


class BaseAccountSchema(BaseModel):
    username: str
    email: Optional[EmailStr]
    phone: Optional[int]
    is_admin: bool


class CreateAccountSchema(BaseAccountSchema):
    password: str = Field(..., min_length=7)


class AccountSchema(BaseAccountSchema):
    id: ObjID = Field(alias='_id')
    date_created: datetime

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime('%Y:%m:%d %H:%M'),
            ObjID: lambda x: str(x)
        }


class Token(BaseModel):
    access_token: str
    refresh_token: str

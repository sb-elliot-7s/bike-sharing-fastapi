from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from custom_objectID import ObjID


class CreateAccountSchema(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: str = Field(..., min_length=7)


class AccountSchema(CreateAccountSchema):
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

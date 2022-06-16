from pydantic import BaseModel


class AddressSchema(BaseModel):
    country: str
    city: str
    street: str
    house: str

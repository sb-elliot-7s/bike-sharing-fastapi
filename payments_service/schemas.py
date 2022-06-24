from typing import Optional

from pydantic import BaseModel, Field
from .constants import PaymentMethodDataType


class PaymentDataSchema(BaseModel):
    amount: float
    description_payment: Optional[str] = Field(None, max_length=128)
    payment_method_data_type: PaymentMethodDataType
    currency: str = 'rub'
    trip_description: str = Field(max_length=128)


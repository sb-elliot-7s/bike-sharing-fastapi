from typing import Optional

from pydantic import BaseModel, Field
from .constants import PaymentMethodDataType, PaymentStatus
from fastapi import Query


class PaymentDataSchema(BaseModel):
    amount: float
    description_payment: Optional[str] = Field(None, max_length=128)
    payment_method_data_type: PaymentMethodDataType
    currency: str = 'rub'
    trip_description: str = Field(..., max_length=128)
    user_fullname: Optional[str] = Field(None, max_length=256)


class FilterPaymentDataSchema(BaseModel):
    limit: Optional[int]
    status: Optional[PaymentStatus]
    payment_method: Optional[PaymentMethodDataType]
    created_at_gte: Optional[str]
    created_at_gt: Optional[str]
    created_at_lte: Optional[str]
    created_at_lt: Optional[str]
    captured_at_gte: Optional[str]
    captured_at_gt: Optional[str]
    captured_at_lte: Optional[str]
    captured_at_lt: Optional[str]

    @staticmethod
    def _transform_key(_key: str):
        return _key[::-1].replace('_', '.', 1)[::-1] if _key.count('_') == 2 \
            else _key

    @property
    def prepare_filter(self):
        return {
            self._transform_key(_key=key): value
            for key, value in self.dict(exclude_none=True).items()
        }

    @classmethod
    def as_query(cls,
                 limit: Optional[int] = Query(None),
                 status: Optional[PaymentStatus] = Query(None),
                 payment_method: Optional[PaymentMethodDataType] = Query(None),
                 created_at_gte: Optional[str] = Query(None),
                 created_at_gt: Optional[str] = Query(None),
                 created_at_lte: Optional[str] = Query(None),
                 created_at_lt: Optional[str] = Query(None),
                 captured_at_gte: Optional[str] = Query(None),
                 captured_at_gt: Optional[str] = Query(None),
                 captured_at_lte: Optional[str] = Query(None),
                 captured_at_lt: Optional[str] = Query(None)):
        return cls(
            limit=limit,
            status=status,
            payment_method=payment_method,
            created_at_gt=created_at_gt,
            created_at_gte=created_at_gte,
            created_at_lte=created_at_lte,
            created_at_lt=created_at_lt,
            captured_at_gte=captured_at_gte,
            captured_at_gt=captured_at_gt,
            captured_at_lte=captured_at_lte,
            captured_at_lt=captured_at_lt
        )


class AmountSchema(BaseModel):
    amount: float
    currency: str

from fastapi import APIRouter, status, Depends
from .schemas import AmountSchema

from account.token_service import TokenService
from permissions import Permission
from .refund_logic import RefundLogic
from .refund_service import RefundService

refund_router = APIRouter(prefix='/refund', tags=['refund'])


@refund_router.post('/{payment_id}', status_code=status.HTTP_201_CREATED)
async def refund_money(
        payment_id: str,
        amount_data: AmountSchema,
        user_account=Depends(Permission(token_service=TokenService()))
):
    return await RefundLogic(refund_service=RefundService()).refund_money(
        payment_id=payment_id,
        amount=amount_data.amount,
        currency=amount_data.currency
    )

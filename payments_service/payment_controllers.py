from fastapi import APIRouter, status, Depends
from .payment_service import PaymentService
from .schemas import PaymentDataSchema, FilterPaymentDataSchema
from permissions import Permission
from account.token_service import TokenService
from .payment_logic import PaymentLogic
from .deps import get_payment_collection

payment_router = APIRouter(prefix='/payment', tags=['payment'])


@payment_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_payment(
        payment_data: PaymentDataSchema,
        user_account=Depends(Permission(token_service=TokenService())),
        payment_collection=Depends(get_payment_collection)
):
    return await PaymentLogic(payment_service=PaymentService()).create_payment(
        user=user_account,
        payment_data=payment_data,
        payment_collection=payment_collection
    )


@payment_router.post('/{payment_id}', status_code=status.HTTP_201_CREATED)
async def confirm_payment(
        payment_id: str,
        user_account=Depends(Permission(token_service=TokenService()))
):
    return await PaymentLogic(payment_service=PaymentService()) \
        .confirm_payment(payment_id=payment_id)


@payment_router.get('/{payment_id}', status_code=status.HTTP_200_OK)
async def payment_info(
        payment_id: str,
        user_account=Depends(Permission(token_service=TokenService()))
):
    return await PaymentLogic(payment_service=PaymentService()) \
        .get_payment_info(payment_id=payment_id)


@payment_router.get('/', status_code=status.HTTP_200_OK)
async def get_filter_payments(
        filter_data: FilterPaymentDataSchema = Depends(FilterPaymentDataSchema.as_query),
        user_account=Depends(Permission(token_service=TokenService()))
):
    return await PaymentLogic(payment_service=PaymentService()) \
        .get_payments_by_filter(_filter=filter_data.prepare_filter)


@payment_router.delete('/{payment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def cancel_payment(
        payment_id: str,
        user_account=Depends(Permission(token_service=TokenService()))
):
    return await PaymentLogic(payment_service=PaymentService()) \
        .cancel_payment(payment_id=payment_id)

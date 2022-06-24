import uuid
from typing import Optional

from yookassa.domain.response import PaymentResponse, PaymentListResponse

from .interfaces.payment_service_interface import PaymentServiceInterface
from yookassa import Payment, Configuration
from configs import get_configs
from .schemas import PaymentDataSchema
from .constants import PaymentStatus
from .create_payment_object import CreatePaymentObject


class PaymentService(PaymentServiceInterface):
    def __init__(self):
        Configuration.account_id = get_configs().you_kassa_account_id
        Configuration.secret_key = get_configs().you_kassa_secret_key

    async def create_payment(self, email: Optional[str], phone: Optional[int],
                             payment_data: PaymentDataSchema):
        try:
            payment_object = await CreatePaymentObject() \
                .get_payment_object(email=email, phone=phone, payment_data=payment_data)
            payment: PaymentResponse = Payment.create(payment_object, str(uuid.uuid4()))
            return payment
        except ...:
            pass

    @staticmethod
    async def confirm_payment(payment_id: str):
        payment: PaymentResponse = Payment \
            .capture(payment_id=payment_id, idempotency_key=str(uuid.uuid4()))
        if payment.status != PaymentStatus.SUCCEEDED:
            """handle error"""
            return
        return payment

    @staticmethod
    async def cancel_payment(payment_id: str):
        payment: PaymentResponse = Payment \
            .cancel(payment_id=payment_id, idempotency_key=str(uuid.uuid4()))

    @staticmethod
    async def get_payment_info(payment_id: str):
        return Payment.find_one(payment_id=payment_id)

    @staticmethod
    async def get_payments_by_filter(_filter: dict):
        try:
            payments: PaymentListResponse = Payment.list(params=_filter)
        except Exception as e:
            """handle error"""
            raise
        return payments

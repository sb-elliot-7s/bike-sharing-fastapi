import uuid
from typing import Optional

from yookassa.domain.response import PaymentResponse

from .interfaces.payment_service_interface import PaymentServiceInterface
from yookassa import Payment, Configuration
from configs import get_configs
from .schemas import PaymentDataSchema
from .constants import PaymentStatus


class PaymentService(PaymentServiceInterface):
    def __init__(self):
        Configuration.account_id = get_configs().you_kassa_account_id
        Configuration.secret_key = get_configs().you_kassa_secret_key

    async def create_payment(self, email: Optional[str], phone: Optional[int],
                             payment_data: PaymentDataSchema):
        try:
            payment_object = {
                'amount': {
                    'value': str(payment_data.amount),
                    'currency': payment_data.currency.upper()
                },
                'payment_method_data': {
                    "type": payment_data.payment_method_data_type.value
                },
                'receipt': {
                    'customer': {
                        'full_name': payment_data.user_fullname,
                        'email': email,
                        'phone': str(phone)
                    },
                    'items': [
                        {
                            'description': payment_data.trip_description,
                            'quantity': '1.00',
                            'amount': {
                                'value': str(payment_data.amount),
                                'currency': payment_data.currency.upper()
                            }
                        }
                    ]
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': "https://www.merchant-website.com/return_url"
                },
                'description': payment_data.description_payment
            }
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
        payment = Payment \
            .cancel(payment_id=payment_id, idempotency_key=str(uuid.uuid4()))

    @staticmethod
    async def get_payment_info(payment_id: str):
        return Payment.find_one(payment_id=payment_id)

    @staticmethod
    async def get_payments_by_filter(_filter: dict):
        try:
            res = Payment.list(params=_filter)
        except Exception as e:
            """handle error"""
            raise
        return res

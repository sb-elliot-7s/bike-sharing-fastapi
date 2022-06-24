import uuid
from .interfaces.payment_service_interface import PaymentServiceInterface
from yookassa import Payment, Configuration
from configs import get_configs
from .schemas import PaymentDataSchema


class PaymentService(PaymentServiceInterface):
    def __init__(self):
        Configuration.account_id = get_configs().you_kassa_account_id
        Configuration.secret_key = get_configs().you_kassa_secret_key

    async def pay_for_the_service(self, payment_data: PaymentDataSchema):
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
                        'full_name': '',
                        'email': '',
                        'phone': ''
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
            payment = Payment.create(payment_object, str(uuid.uuid4()))

        except ...:
            pass

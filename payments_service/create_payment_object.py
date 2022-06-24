from typing import Optional

from configs import get_configs
from payments_service.schemas import PaymentDataSchema


class CreatePaymentObject:
    @staticmethod
    async def get_payment_object(email: Optional[str], phone: Optional[str],
                                  payment_data: PaymentDataSchema):
        return {
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
                'return_url': get_configs().return_url
            },
            'description': payment_data.description_payment
        }

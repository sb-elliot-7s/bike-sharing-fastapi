from payments_service.interfaces.refund_service_interface import RefundServiceInterface
from .constants import PaymentStatus
from yookassa import Refund
import uuid


class RefundService(RefundServiceInterface):
    @staticmethod
    async def refund_money(payment_id: str, amount: float, currency: str):
        refund_object = {
            "amount": {
                "value": str(amount),
                "currency": currency.upper()
            },
            "payment_id": payment_id
        }
        refund = Refund.create(refund_object, idempotency_key=str(uuid.uuid4()))
        if refund.status != PaymentStatus.SUCCEEDED.value:
            print('error')
            return
        return refund

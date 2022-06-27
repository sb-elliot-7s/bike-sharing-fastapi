from time import time

from payments_service.interfaces.refund_service_interface import RefundServiceInterface
from .constants import PaymentStatus
from yookassa import Refund
import uuid


class RefundService(RefundServiceInterface):
    @staticmethod
    async def _get_updated_data(user_id: str, payment_id: str):
        return {
            'filter': {'user_id': user_id, 'youkassa_payment_id': payment_id},
            'update': {'$set': {'status_payment': PaymentStatus.CANCELED.value, 'timestamp_update': time()}}
        }

    async def refund_money(self, user_id: str, payment_id: str, amount: float, currency: str,
                           payment_collection):
        refund_object = {"amount": {"value": str(amount), "currency": currency.upper()},
                         "payment_id": payment_id}
        refund = Refund.create(refund_object, idempotency_key=str(uuid.uuid4()))
        if refund.status != PaymentStatus.SUCCEEDED.value:
            """handle error"""
            return
        await payment_collection.update_one(**await self._get_updated_data(user_id, payment_id))
        return refund

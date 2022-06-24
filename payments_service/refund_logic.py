from .interfaces.refund_service_interface import RefundServiceInterface


class RefundLogic:
    def __init__(self, refund_service: RefundServiceInterface):
        self._refund_service = refund_service

    async def refund_money(self, payment_id: str, amount: float, currency: str):
        return await self._refund_service \
            .refund_money(payment_id=payment_id, amount=amount, currency=currency)

from .interfaces.payment_service_interface import PaymentServiceInterface
from .schemas import PaymentDataSchema


class PaymentLogic:
    def __init__(self, payment_service: PaymentServiceInterface):
        self._payment_service = payment_service

    async def create_payment(
            self, payment_collection, user, payment_data: PaymentDataSchema
    ):
        return await self._payment_service \
            .create_payment(user=user, payment_data=payment_data,
                            payment_collection=payment_collection)

    async def confirm_payment(self, payment_id: str):
        return await self._payment_service.confirm_payment(
            payment_id=payment_id
        )

    async def cancel_payment(self, payment_id: str):
        return await self._payment_service.cancel_payment(payment_id=payment_id)

    async def get_payment_info(self, payment_id: str):
        return await self._payment_service.get_payment_info(
            payment_id=payment_id
        )

    async def get_payments_by_filter(self, _filter: dict):
        return await self._payment_service.get_payments_by_filter(
            _filter=_filter
        )

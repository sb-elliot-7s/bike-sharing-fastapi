from abc import ABC, abstractmethod
from ..schemas import PaymentDataSchema


class PaymentServiceInterface(ABC):
    @abstractmethod
    async def create_payment(self, payment_collection, user, payment_data: PaymentDataSchema):
        pass

    @staticmethod
    @abstractmethod
    async def confirm_payment(payment_id: str): pass

    @staticmethod
    @abstractmethod
    async def cancel_payment(payment_id: str): pass

    @staticmethod
    @abstractmethod
    async def get_payment_info(payment_id: str): pass

    @staticmethod
    @abstractmethod
    async def get_payments_by_filter(_filter: dict): pass

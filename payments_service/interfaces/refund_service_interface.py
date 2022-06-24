from abc import ABC, abstractmethod


class RefundServiceInterface(ABC):
    @staticmethod
    @abstractmethod
    async def refund_money(payment_id: str, amount: float, currency: str):
        pass

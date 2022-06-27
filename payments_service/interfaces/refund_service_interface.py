from abc import ABC, abstractmethod


class RefundServiceInterface(ABC):
    @abstractmethod
    async def refund_money(self, user_id: str, payment_id: str, amount: float,
                           currency: str, payment_collection):
        pass

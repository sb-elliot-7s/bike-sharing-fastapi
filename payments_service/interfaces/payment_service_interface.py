from abc import ABC, abstractmethod
from ..schemas import PaymentDataSchema


class PaymentServiceInterface(ABC):
    @abstractmethod
    async def pay_for_the_service(self, payment_data: PaymentDataSchema):
        pass

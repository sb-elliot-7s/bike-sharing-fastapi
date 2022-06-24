from enum import Enum


class PaymentMethodDataType(Enum):
    BANK_CARD = 'bank_card'
    YOO_MONEY = 'yoo_money'
    SBERBANK = 'sberbank'
    ALFABANK = 'alfabank'
    TINKOFF_BANK = 'tinkoff_bank'
    QIWI = 'qiwi'
    MOBILE_BALANCE = 'mobile_balance'
    SBP = 'sbp'
    CASH = 'cash'
    INSTALLMENTS = 'installments'


class PaymentStatus(Enum):
    PENDING = 'pending'
    WAITING_FOR_CAPTURE = 'waiting_for_capture'
    SUCCEEDED = 'succeeded'
    CANCELED = 'canceled'

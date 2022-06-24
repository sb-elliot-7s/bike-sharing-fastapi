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

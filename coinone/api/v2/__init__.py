import typing

from .account import Account
from .order import Order
from ...core import CoinoneV2 as _CoinoneV2


class CoinoneV2(_CoinoneV2):
    @property
    def account(self) -> Account:
        return Account(self.__getattr__('account'))

    @property
    def order(self) -> Order:
        return Order(self.__getattr__('order'))

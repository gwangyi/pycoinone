import typing

from .account import Account
from ...core import CoinoneV1 as _CoinoneV1


class CoinoneV1(_CoinoneV1):
    @property
    def account(self) -> Account:
        return Account(self.__getattr__('account'))

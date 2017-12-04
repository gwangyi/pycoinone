import typing

from .account import Account
from .order import Order
from ..base import magic_result, delegated_getter
from ..common.public import PublicApiMixin
from ...core import CoinoneV1 as _CoinoneV1, Coinone


class CoinoneV1(PublicApiMixin):
    def __init__(self, access_token: str) -> None:
        super().__init__()
        self._api = _CoinoneV1(access_token)

    @property
    def account(self) -> Account:
        return Account(self._api.account)

    @property
    def order(self) -> Order:
        return Order(self._api.order)

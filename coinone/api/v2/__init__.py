import typing

from .account import Account
from .order import Order
from ..base import magic_result, delegated_getter
from ..common.public import PublicApiMixin
from ...core import CoinoneV2 as _CoinoneV2


class CoinoneV2(PublicApiMixin):
    def __init__(self, access_token: str, secret_key: str) -> None:
        super().__init__()
        self._api = _CoinoneV2(access_token, secret_key)

    @property
    def account(self) -> Account:
        return Account(self._api.account)

    @property
    def order(self) -> Order:
        return Order(self._api.order)

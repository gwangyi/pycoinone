import typing

from .account import Account
from .order import Order
from .transaction import Transaction
from ..base import magic_result, delegated_getter
from ..common.public import PublicApiMixin
from ...core import CoinoneV1 as Api, Coinone


class CoinoneV1(PublicApiMixin):
    def __init__(self, access_token: str) -> None:
        super().__init__()
        self._api = Api(access_token)

    @property
    def account(self) -> Account:
        return Account(self._api.account)

    @property
    def order(self) -> Order:
        return Order(self._api.order)

    @property
    def transaction(self) -> Transaction:
        return Transaction(self._api.transaction)

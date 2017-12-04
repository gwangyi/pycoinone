import typing
from ..base import ApiResult, ApiMagic, magic_method, post, form_data
from ..common.transaction import KrwHistory


class CoinTransactionEntry(ApiMagic):
    txid: str
    type: str
    from_: str
    to: str
    confirmations: int
    quantity: float
    timestamp: int


class CoinTransactions(ApiResult):
    transactions: typing.List[CoinTransactionEntry]


class SendCoin(ApiResult):
    txid: str


class KrwMagic(ApiMagic):
    @magic_method
    def history(self) -> KrwHistory:
        ...


class Transaction(ApiMagic):
    @magic_method
    def auth_number(self, type: str) -> ApiResult:
        ...

    @magic_method
    def history(self, currency: str) -> CoinTransactions:
        ...

    @property
    def krw(self) -> KrwMagic:
        return KrwMagic(self.__getattr__('krw'))

    @magic_method
    def coin(self, currency: str, address: str, auth_number: int, qty: float,
             type: str, from_address: str) -> ApiResult:
        ...

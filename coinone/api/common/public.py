import typing
from ..base import ApiResult, ApiMagic, magic_result, delegated
from ...core import Coinone


class OrderbookEntry(ApiMagic):
    price: int
    qty: float


class Orderbook(ApiResult):
    ask: typing.List[OrderbookEntry]
    bid: typing.List[OrderbookEntry]
    timestamp: int
    currency: str


class TradesEntry(ApiMagic):
    price: int
    qty: float
    timestamp: int


class Trades(ApiResult):
    timestamp: int
    completeOrders: typing.List[TradesEntry]
    currency: str


class Ticker(ApiResult):
    high: int
    low: int
    last: int
    first: int
    volume: float
    timestamp: int
    currency: str


class PublicApiMixin:
    def __init__(self) -> None:
        self._public_api = Coinone()

    @magic_result
    @delegated('_public_api')
    def orderbook(self, currency: str) -> Orderbook:
        ...

    @magic_result
    @delegated('_public_api')
    def trades(self, currency: str, period: str) -> Trades:
        ...

    @magic_result
    @delegated('_public_api')
    def ticker(self, currency: str) -> Ticker:
        ...

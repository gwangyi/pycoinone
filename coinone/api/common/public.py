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


class _Ticker(ApiMagic):
    high: int
    low: int
    last: int
    first: int
    volume: float
    yesterday_high: int
    yesterday_low: int
    yesterday_last: int
    yesterday_first: int
    yesterday_volume: float
    currency: str


class Ticker(_Ticker, ApiResult):
    timestamp: int


class TickerAll(ApiResult):
    btc: _Ticker
    bch: _Ticker
    eth: _Ticker
    etc: _Ticker
    xrp: _Ticker
    qtum: _Ticker
    iota: _Ticker
    ltc: _Ticker
    btg: _Ticker
    timestamp: int


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

    def ticker_all(self) -> TickerAll:
        return TickerAll(self._public_api.ticker(currency='all'))

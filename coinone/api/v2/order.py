import typing
from ..base import (ApiResult, CurrencyMagic, magic_method, post, form_data,
                    currency_method)
from ..common.order import OrderId, CompleteOrders, LimitOrders
from ..common.enums import Currency, OrderType


class Order(CurrencyMagic):
    @currency_method
    @magic_method
    def cancel(self, order_id: str, price: int, qty: float,
               is_ask: OrderType,
               currency: Currency=Currency.BTC) -> ApiResult:
        ...

    @currency_method
    @magic_method
    def limit_buy(self, price: int, qty: float,
                  currency: Currency=Currency.BTC) -> OrderId:
        ...

    @currency_method
    @magic_method
    def limit_sell(self, price: int, qty: float,
                   currency: Currency=Currency.BTC) -> OrderId:
        ...

    @currency_method
    @magic_method
    def complete_orders(self, currency: Currency=Currency.BTC)\
            -> CompleteOrders:
        ...

    @currency_method
    @magic_method
    def limit_orders(self, currency: Currency=Currency.BTC)\
            -> LimitOrders:
        ...

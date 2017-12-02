import typing
from ..base import ApiResult, ApiMagic, magic_method, post, form_data
from ..common.order import OrderId, CompleteOrders, LimitOrders


class Order(ApiMagic):
    @magic_method
    def cancel(self, order_id: str, price: int, qty: float, is_ask: int,
               currency: str="btc") -> ApiResult:
        ...

    @magic_method
    def limit_buy(self, price: int, qty: float, currency: str="btc")\
            -> OrderId:
        ...

    @magic_method
    def limit_sell(self, price: int, qty: float, currency: str="btc")\
            -> OrderId:
        ...

    @magic_method
    def complete_orders(self, currency: str="btc") -> CompleteOrders:
        ...

    @magic_method
    def limit_orders(self, currency: str="btc") -> LimitOrders:
        ...

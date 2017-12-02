import typing
from ..base import ApiResult, ApiMagic, magic_method, post, form_data
from ..common.order import OrderId, CompleteOrders, LimitOrders


class Order(ApiMagic):
    @post
    @form_data
    @magic_method
    def cancel(self, order_id: str, price: int, qty: float, is_ask: int)\
            -> ApiResult:
        ...

    @post
    @form_data
    @magic_method
    def limit_buy(self, price: int, qty: float) -> OrderId:
        ...

    @post
    @form_data
    @magic_method
    def limit_sell(self, price: int, qty: float) -> OrderId:
        ...

    @magic_method
    def complete_orders(self) -> CompleteOrders:
        ...

    @magic_method
    def limit_orders(self) -> LimitOrders:
        ...

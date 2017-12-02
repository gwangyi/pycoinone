import typing
from ..base import ApiResult, ApiMagic


class OrderId(ApiResult):
    orderId: str


class CompleteOrder(ApiMagic):
    timestamp: int
    price: int
    qty: float
    type: str
    feeRate: float
    fee: float
    orderId: str


class CompleteOrders(ApiResult):
    completeOrders: typing.List[CompleteOrder]


class LimitOrder(ApiMagic):
    index: int
    timestamp: int
    price: int
    qty: float
    orderId: str
    type: str
    feeRate: float


class LimitOrders(ApiResult):
    limitOrders: typing.List[LimitOrder]

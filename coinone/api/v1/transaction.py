import typing
from ..base import ApiResult, ApiMagic, magic_method, post, form_data
from ..common.transaction import KrwHistory


class BtcHistoryEntry(ApiMagic):
    transactionId: str
    type: str
    from_: str
    to: str
    confirmations: int
    quantity: float
    timestamp: str


class BtcHistory(ApiResult):
    btcHistory: typing.List[BtcHistoryEntry]


class Transaction(ApiMagic):
    @magic_method
    def auth_number(self, type: str) -> ApiResult:
        ...

    @magic_method
    def btc_get(self) -> BtcHistory:
        ...

    @magic_method
    def krw_get(self) -> KrwHistory:
        ...

    @form_data
    @magic_method
    def btc_post(self, address: str, auth_number: int, qty: float,
                 type: str, from_address: str) -> ApiResult:
        ...

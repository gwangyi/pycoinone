import typing
from ..base import ApiResult, ApiMagic


class KrwHistoryEntry(ApiMagic):
    bankCode: int
    accountNumber: str
    depositor: str
    amount: int
    processLevel: int
    timestamp: int


class KrwHistory(ApiResult):
    krwHistory: typing.List[KrwHistoryEntry]

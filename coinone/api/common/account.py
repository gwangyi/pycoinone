import typing
from ..base import ApiResult, ApiMagic


_T_currency = typing.TypeVar('_T_currency', int, float)


class CurrencyInfo(ApiMagic, typing.Generic[_T_currency]):
    avail: _T_currency
    balance: _T_currency


class NormalWallet(ApiMagic):
    balance: float
    label: str


class VirtualAccountInfo(ApiMagic):
    depositor: str
    accountNumber: str
    bankName: str


class MobileInfo(ApiMagic):
    userName: str
    phoneNumber: str
    phoneCorp: str
    isAuthenticated: bool


class BankInfo(ApiMagic):
    depositor: str
    bankCode: str
    accountNumber: str
    isAuthenticated: bool


class EmailInfo(ApiMagic):
    isAuthenticated: bool
    email: str


class FeeRate(ApiMagic):
    maker: float
    taker: float


class VirtualAccount(ApiResult):
    accountNumber: str
    depositor: str
    bankName: str

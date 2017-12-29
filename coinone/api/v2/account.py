import typing
from ..base import ApiResult, ApiMagic, magic_method
from ..common.account import (CurrencyInfo, NormalWallet, VirtualAccountInfo,
                              MobileInfo, BankInfo, EmailInfo, FeeRate,
                              VirtualAccount)


class BtcDepositAddress(ApiResult):
    walletAddress: str


class Balance(ApiResult):
    btc: CurrencyInfo[float]
    bch: CurrencyInfo[float]
    eth: CurrencyInfo[float]
    etc: CurrencyInfo[float]
    xrp: CurrencyInfo[float]
    qtum: CurrencyInfo[float]
    iota: CurrencyInfo[float]
    ltc: CurrencyInfo[float]
    btg: CurrencyInfo[float]
    krw: CurrencyInfo[int]
    normalWallets: typing.List[NormalWallet]


class DailyBalanceInfo(ApiMagic):
    timestamp: int
    value: int
    krw: int
    btc: float
    bch: float
    eth: float
    etc: float
    xrp: float
    qtum: float
    iota: float
    ltc: float
    btg: float


class DailyBalance(ApiResult):
    dailyBalance: typing.List[DailyBalanceInfo]


class WalletAddress(ApiMagic):
    btc: str
    bch: str
    eth: str
    etc: str
    xrp: str
    xrp_tag: str
    qtum: str
    iota: str
    ltc: str
    btg: str


class DepositAddress(ApiResult):
    walletAddress: WalletAddress


class FeeRates(ApiMagic):
    btc: FeeRate
    bch: FeeRate
    eth: FeeRate
    etc: FeeRate
    xrp: FeeRate
    qtum: FeeRate
    iota: FeeRate
    ltc: FeeRate
    btg: FeeRate


class _UserInfo(ApiMagic):
    virtualAccountInfo: VirtualAccountInfo
    mobileInfo: MobileInfo
    bankInfo: BankInfo
    emailInfo: EmailInfo
    securityLevel: int
    feeRate: FeeRates


class UserInfo(ApiResult):
    userInfo: _UserInfo


class Account(ApiMagic):
    @magic_method
    def btc_deposit_address(self) -> BtcDepositAddress:
        ...

    @magic_method
    def balance(self) -> Balance:
        ...

    @magic_method
    def daily_balance(self) -> DailyBalance:
        ...

    @magic_method
    def user_info(self) -> UserInfo:
        ...

    @magic_method
    def virtual_account(self) -> VirtualAccount:
        ...

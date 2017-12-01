import typing
from ..base import ApiResult, ApiMagic, magic_method
from ..common.account import (CurrencyInfo, NormalWallet, VirtualAccountInfo,
                              MobileInfo, BankInfo, EmailInfo, FeeRate,
                              VirtualAccount)


class BtcDepositAddress(ApiResult):
    walletAddress: str


class Balance(ApiResult):
    btc: CurrencyInfo[float]
    krw: CurrencyInfo[int]
    normalWallets: typing.List[NormalWallet]


class DailyBalanceInfo(ApiMagic):
    timestamp: int
    value: int
    krw: int
    btc: float


class DailyBalance(ApiResult):
    dailyBalance: typing.List[DailyBalanceInfo]


class _UserInfo(ApiMagic):
    virtualAccountInfo: VirtualAccountInfo
    mobileInfo: MobileInfo
    bankInfo: BankInfo
    emailInfo: EmailInfo
    securityLevel: int
    feeRate: FeeRate


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

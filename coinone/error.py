import enum
import typing
import collections


class CoinoneErrorCode(enum.Enum):
    BlockedUserAccess = (4, 'Blocked user access')
    AccessTokenMissing = (11, 'Access token is missing')
    InvalidAccessToken = (12, 'Invalid access token')
    PermissionDenied = (40, 'Invalid API permission')
    AuthenticateError = (50, 'Authenticate error')
    InvalidAPI = (51, 'Invalid API')
    DeprecatedAPI = (52, 'Deprecated API')
    TwoFactorAuthFail = (53, 'Two Factor Auth Fail')
    SessionExpired = (100, 'Session expired')
    InvalidFormat = (101, 'Invalid format')
    IdNotExist = (102, "ID is not exist")
    LackOfBalance = (103, "Lack of Balance")
    OrderIdNotExist104 = (104, "Order id is not exist")
    PriceIsNotCorrect = (105, "Price is not correct")
    LockingError106 = (106, "Locking error")
    ParameterError = (107, "Parameter error")
    OrderIdNotExist111 = (111, "Order id is not exist")
    CancelFailed = (112, "Cancel failed")
    TooLowQuantity = (113, "Quantity is too low(ETH, ETC > 0.01)")
    V2PayloadMissing = (120, "V2 API payload is missing")
    V2SignatureMissing = (121, "V2 API signature is missing")
    V2NonceMissing = (122, "V2 API nonce is missing")
    V2SignatureMismatch = (123, "V2 API signature is not correct")
    V2NonceNegative = (130, "V2 API Nonce value must be a positive integer")
    V2NonceMismatch = (131, "V2 API Nonce is must be bigger then last nonce")
    V2BodyCorrupted = (132, "V2 API body is corrupted")
    TooManyLimitOrders = (141, "Too many limit orders")
    V1WrongAccessToken = (150, "It's V1 API. "
                               "V2 Access token is not acceptable")
    V2WrongAccessToken = (151, "It's V2 API. "
                               "V1 Access token is not acceptable")
    WalletError = (200, "Wallet Error")
    LimitationError202 = (202, "Limitation error")
    LimitationError210 = (210, "Limitation error")
    LimitationError220 = (220, "Limitation error")
    LimitationError221 = (221, "Limitation error")
    MobileAuthError310 = (310, "Mobile auth error")
    NeedMobileAuth = (311, "Need mobile auth")
    BadName = (312, "Name is not correct")
    BadPhoneNumber330 = (330, "Phone number error")
    PageNotFound = (404, "Page not found error")
    ServerError = (405, "Server error")
    LockingError444 = (444, "Locking error")
    EmailError500 = (500, "Email error")
    EmailError501 = (501, "Email error")
    MobileAuthError777 = (777, "Mobile auth error")
    BadPhoneNumber778 = (778, "Phone number error")
    AppNotFound = (1202, "App not found")
    AlreadyRegistered = (1203, "Already registered")
    InvalidAccess = (1204, "Invalid access")
    APIKeyError = (1205, "API Key error")
    UserNotFound1206 = (1206, "User not found")
    UserNotFound1207 = (1207, "User not found")
    UserNotFound1208 = (1208, "User not found")
    UserNotFound1209 = (1209, "User not found")

    @typing.no_type_check
    def __new__(cls, code: int, desc: str) -> 'CoinoneErrorCode':
        self = object.__new__(cls)
        self._value_ = code
        self.__doc__ = desc
        return self

    def __init__(cls, code: int, desc: typing.Optional[str] = None) -> None:
        pass

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}.{self.name}: '\
               f'{self.__doc__} ({self.value})>'


class CoinoneError(RuntimeError):
    _error_map: typing.Dict[typing.Container[int],
                            typing.Type['CoinoneError']]\
            = collections.OrderedDict()

    @staticmethod
    def register(*error_code: CoinoneErrorCode)\
            -> typing.Callable[[typing.Type['CoinoneError']],
                               typing.Type['CoinoneError']]:
        def decorator(error_type: typing.Type['CoinoneError'])\
                -> typing.Type['CoinoneError']:
            codes = tuple(code.value for code in error_code)
            CoinoneError._error_map[codes] = error_type
            return error_type

        return decorator

    def __new__(cls, code: int, message: typing.Optional[str]=None)\
            -> 'CoinoneError':
        if cls is CoinoneError:
            for k, v in CoinoneError._error_map.items():
                if code in k:
                    return v(code, message)
        return typing.cast(CoinoneError, RuntimeError.__new__(cls))

    def __init__(self, code: int, message: typing.Optional[str]=None) -> None:
        ecode = CoinoneErrorCode(code)
        if message is None:
            super().__init__(f'[Error {code}] {ecode.__doc__}')
        else:
            super().__init__(f'[Error {code}] {message}')
        self.code = code


@CoinoneError.register(CoinoneErrorCode.APIKeyError)
class APIKeyErrorError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.AccessTokenMissing)
class AccessTokenMissingError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.AlreadyRegistered)
class AlreadyRegisteredError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.AppNotFound)
class AppNotFoundError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.AuthenticateError)
class AuthenticateErrorError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.BadName)
class BadNameError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.BadPhoneNumber330,
                       CoinoneErrorCode.BadPhoneNumber778)
class BadPhoneNumberError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.BlockedUserAccess)
class BlockedUserAccessError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.CancelFailed)
class CancelFailedError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.DeprecatedAPI)
class DeprecatedAPIError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.EmailError500,
                       CoinoneErrorCode.EmailError501)
class EmailErrorError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.IdNotExist)
class IdNotExistError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.InvalidAPI)
class InvalidAPIError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.InvalidAccess)
class InvalidAccessError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.InvalidAccessToken)
class InvalidAccessTokenError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.InvalidFormat)
class InvalidFormatError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.LackOfBalance)
class LackOfBalanceError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.LimitationError202,
                       CoinoneErrorCode.LimitationError210,
                       CoinoneErrorCode.LimitationError220,
                       CoinoneErrorCode.LimitationError221)
class LimitationError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.LockingError106,
                       CoinoneErrorCode.LockingError444)
class LockingError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.MobileAuthError310,
                       CoinoneErrorCode.MobileAuthError777)
class MobileAuthErrorError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.NeedMobileAuth)
class NeedMobileAuthError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.OrderIdNotExist104,
                       CoinoneErrorCode.OrderIdNotExist111)
class OrderIdNotExistError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.PageNotFound)
class PageNotFoundError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.ParameterError)
class ParameterErrorError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.PermissionDenied)
class PermissionDeniedError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.PriceIsNotCorrect)
class PriceIsNotCorrectError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.ServerError)
class ServerErrorError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.SessionExpired)
class SessionExpiredError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.TooLowQuantity)
class TooLowQuantityError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.TooManyLimitOrders)
class TooManyLimitOrdersError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.TwoFactorAuthFail)
class TwoFactorAuthFailError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.UserNotFound1206,
                       CoinoneErrorCode.UserNotFound1207,
                       CoinoneErrorCode.UserNotFound1208,
                       CoinoneErrorCode.UserNotFound1209)
class UserNotFoundError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.V1WrongAccessToken)
class V1WrongAccessTokenError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.V2BodyCorrupted)
class V2BodyCorruptedError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.V2NonceMismatch)
class V2NonceMismatchError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.V2NonceMissing)
class V2NonceMissingError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.V2NonceNegative)
class V2NonceNegativeError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.V2PayloadMissing)
class V2PayloadMissingError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.V2SignatureMismatch)
class V2SignatureMismatchError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.V2SignatureMissing)
class V2SignatureMissingError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.V2WrongAccessToken)
class V2WrongAccessTokenError(CoinoneError):
    pass


@CoinoneError.register(CoinoneErrorCode.WalletError)
class WalletErrorError(CoinoneError):
    pass

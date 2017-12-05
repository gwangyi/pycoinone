import typing
import functools
from .common.enums import Currency
from ..core import to_html


_T = typing.TypeVar('_T')


class ApiMagic:
    __origin__: typing.Type
    __args__: typing.Sequence[typing.Type]
    __annotations__: typing.Dict[str, typing.Type] = {}
    _subs: typing.Dict[typing.Any, typing.Type] = {}

    _annotations: typing.Dict[str, typing.Type] = {}

    @classmethod
    def _substitute(cls) -> typing.Dict[typing.Any, typing.Type]:
        if hasattr(cls, '__origin__') and hasattr(cls, '__args__'):
            subs = dict(cls.__origin__._subs)
            subs.update({p: a for p, a in zip(cls.__origin__.__parameters__,
                                              cls.__args__)})
            return subs
        return {}

    @classmethod
    def __init_subclass__(cls, *args: typing.Any, **kwargs: typing.Any)\
            -> None:
        cls._annotations = dict((k, v) for base in cls.__bases__
                                if hasattr(base, '__annotations__')
                                for k, v in base.__annotations__.items())
        cls._annotations.update(cls.__annotations__)

    def __init__(self, obj: typing.Any) -> None:
        self._obj = obj

    def __getattr__(self, key: str) -> typing.Any:
        obj = getattr(self._obj, key)
        if key in self._annotations:
            tp = self._annotations[key]
            tp = self._subs.get(tp, tp)
            if hasattr(tp, '__origin__') and\
                    getattr(tp, '__origin__') is typing.List:
                return [getattr(tp, '__args__')[0](elem) for elem in obj]
            if issubclass(tp, ApiMagic):
                subs = tp._substitute()
                res = subs.get(tp, tp)(obj)
                res._subs = subs
            else:
                res = tp(obj)
            return res
        else:
            return obj

    def _repr_html_(self) -> str:
        return to_html({
            key: getattr(self, key)
            for key in self._annotations if not key.startswith('_')
        })


class CurrencyMagic(ApiMagic):
    _currency = Currency.BTC

    def __getitem__(self: _T, currency: Currency) -> _T:
        return _set_currency(self, currency)


class ApiResult(ApiMagic):
    result: str
    errorCode: str


_T_magic = typing.TypeVar('_T_magic', bound=ApiMagic, covariant=True)


def magic_method(fn: _T) -> _T:
    fn_ = typing.cast(typing.Callable[..., typing.Any], fn)
    ret_type: ApiMagic = fn_.__annotations__['return']
    name = fn_.__name__
    def_kwargs = {}

    prefix, *postfix = name.rsplit('_', 2)
    if postfix and postfix[0] in ('get', 'post'):
        def_kwargs['_method_'] = postfix[0]
        name = prefix

    @functools.wraps(fn_)
    def wrapper(self: typing.Any, *args: typing.Any, **kwargs: typing.Any)\
            -> _T_magic:
        kwargs_ = dict(def_kwargs)
        kwargs_.update(kwargs)
        if hasattr(self, '__getattr__'):
            obj: typing.Any = self.__getattr__(name)(*args, **kwargs_)
            return typing.cast(_T_magic, ret_type(obj))
        else:
            raise AttributeError(name)

    return typing.cast(_T, wrapper)


def _add_param(fn: _T, **kwargs: typing.Any) -> _T:
    fn_ = typing.cast(typing.Callable[..., typing.Any], fn)

    @functools.wraps(fn_)
    def wrapper(*args: typing.Any, **kwargs_: typing.Any) -> typing.Any:
        p = dict(kwargs)
        p.update(kwargs_)

        return fn_(*args, **p)

    return typing.cast(_T, wrapper)


def delegated_getter(name: str) -> typing.Callable[[_T], _T]:
    def decorator(fn: _T) -> _T:
        fn_ = typing.cast(typing.Callable, fn)

        @functools.wraps(fn_)
        def wrapper(self: typing.Any) -> typing.Any:
            return getattr(getattr(self, name), fn_.__name__)

        return typing.cast(_T, wrapper)
    return decorator


def delegated(name: str) -> typing.Callable[[_T], _T]:
    def decorator(fn: _T) -> _T:
        fn_ = typing.cast(typing.Callable, fn)

        @functools.wraps(fn_)
        def wrapper(self: typing.Any, *args: typing.Any,
                    **kwargs: typing.Any) -> typing.Any:
            return getattr(getattr(self, name), fn_.__name__)(*args, **kwargs)

        return typing.cast(_T, wrapper)
    return decorator


def magic_result(fn: _T) -> _T:
    fn_ = typing.cast(typing.Callable, fn)
    ret_type: typing.Type = fn_.__annotations__['return']

    @functools.wraps(fn_)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return ret_type(fn_(*args, **kwargs))

    return typing.cast(_T, wrapper)


def post(fn: _T) -> _T:
    return _add_param(fn, _method_='post')


def form_data(fn: _T) -> _T:
    return _add_param(fn, _payload_='data')


def currency_method(fn: _T) -> _T:
    fn_ = typing.cast(typing.Callable, fn)

    @functools.wraps(fn_)
    def wrapper(self: ApiMagic, *args: typing.Any, **kwargs: typing.Any)\
            -> typing.Any:
        if hasattr(self, '_currency') and 'currency' not in kwargs:
            kwargs['currency'] = getattr(self, '_currency')
        return fn_(self, *args, **kwargs)

    return typing.cast(_T, wrapper)


def _set_currency(self: _T, currency: Currency) -> _T:
    if isinstance(self, CurrencyMagic):
        obj = typing.cast(_T, self.__class__(self._obj))
        if isinstance(obj, CurrencyMagic):
            obj._currency = currency
        return obj
    return self

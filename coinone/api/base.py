import typing
import functools
from ..core import to_html


class ApiMagic:
    __origin__: typing.Type
    __args__: typing.Sequence[typing.Type]
    __annotations__: typing.Dict[str, typing.Type] = {}
    _subs: typing.Dict[typing.Any, typing.Type] = {}

    @classmethod
    def _substitute(cls) -> typing.Dict[typing.Any, typing.Type]:
        if hasattr(cls, '__origin__') and hasattr(cls, '__args__'):
            subs = dict(cls.__origin__._subs)
            subs.update({p: a for p, a in zip(cls.__origin__.__parameters__,
                                              cls.__args__)})
            return subs
        return {}

    def __init__(self, obj: typing.Any) -> None:
        self._obj = obj

    def __getattr__(self, key: str) -> typing.Any:
        obj = getattr(self._obj, key)
        if key in self.__annotations__:
            tp = self.__annotations__[key]
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
            for key in self.__annotations__
        })


class ApiResult(ApiMagic):
    result: str
    errorCode: str


_T = typing.TypeVar('_T')
_T_magic = typing.TypeVar('_T_magic', bound=ApiMagic, covariant=True)


def magic_method(fn: _T) -> _T:
    fn_ = typing.cast(typing.Callable[..., typing.Any], fn)
    ret_type: ApiMagic = fn_.__annotations__['return']
    name = fn_.__name__

    @functools.wraps(fn_)
    def wrapper(self: typing.Any, *args: typing.Any, **kwargs: typing.Any)\
            -> _T_magic:
        if hasattr(self, '__getattr__'):
            obj: typing.Any = self.__getattr__(name)(*args, **kwargs)
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


def post(fn: _T) -> _T:
    return _add_param(fn, _method_='post')


def form_data(fn: _T) -> _T:
    return _add_param(fn, _payload_='data')

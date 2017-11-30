from . import raw, error
import typing
import time
import threading
import functools


def _process_error(path: str, response: typing.Mapping[str, typing.Any])\
        -> typing.Mapping[str, typing.Any]:
    if 'result' not in response:
        raise RuntimeError(f"Ugly-shaped result: {repr(response)}")

    if response['result'] != 'success':
        code = int(response['errorCode'])
        msg = response.get('errorMessage',
                           error.CoinoneErrorCode(code).__doc__)
        raise error.CoinoneError(code, f'{msg} at {path}')
    return response


_AnyFn = typing.Callable[..., typing.Any]


def _rate_limited(count: int, period: float)\
        -> typing.Callable[[_AnyFn], _AnyFn]:
    lock = threading.Lock()
    last_call_time: float = 0
    left_call_count = count

    def decorator(fn: _AnyFn) -> _AnyFn:
        @functools.wraps(fn)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            nonlocal last_call_time, left_call_count

            now = time.time()
            lock.acquire()
            if last_call_time < now - period or left_call_count <= 0:
                if left_call_count <= 0:
                    time.sleep(last_call_time + period - now)
                last_call_time = time.time()
                left_call_count = count
            left_call_count -= 1
            lock.release()

            return fn(*args, **kwargs)

        return wrapper

    return decorator


class _Coinone(raw.Coinone):
    def _execute(self, path: str, **kwargs: typing.Any)\
            -> typing.Mapping[str, typing.Any]:
        return _process_error(path, super()._execute(path, **kwargs))


class Coinone(_Coinone):
    @_rate_limited(90, 60)
    def _execute(self, path: str, **kwargs: typing.Any)\
            -> typing.Mapping[str, typing.Any]:
        return super()._execute(path, **kwargs)


class CoinoneV1(_Coinone, raw.CoinoneV1):
    @_rate_limited(6, 1)
    def _execute(self, path: str, **kwargs: typing.Any)\
            -> typing.Mapping[str, typing.Any]:
        return super()._execute(path, **kwargs)


class CoinoneV2(_Coinone, raw.CoinoneV2):
    @_rate_limited(6, 1)
    def _execute(self, path: str, **kwargs: typing.Any)\
            -> typing.Mapping[str, typing.Any]:
        return super()._execute(path, **kwargs)

from . import raw, error
import typing
import time
import threading
import functools
import json
import collections
import html


def to_html(obj: typing.Any) -> str:
    if isinstance(obj, dict):
        head_row =\
                '<tr><th style="width: auto; white-space: nowrap">Field</th>'\
                '<th style="width: 100%">Value</th>'
        return "".join((
            elem for elems in [
                [
                    '<table style="table-layout: auto; width: 100%"><thead>',
                    head_row,
                    "</tr></thead><tbody>"
                ],
                (
                    '<tr><td><pre style="width: auto; white-space: nowrap">'
                    '{field}</pre></td>'
                    "<td>{value}</td></tr>".format(
                        field=key,
                        value=to_html(value)
                    ) for key, value in obj.items()
                ),
                [
                    "</tbody></table>"
                    '</div>'
                ]
            ] for elem in elems))
    elif isinstance(obj, list):
        return "".join(term for terms in [
            ['<ul style="max-height: 20em; overflow-y: auto">'],
            ("<li>" + to_html(elem) + "</li>" for elem in obj),
            ["</ul>"]
        ] for term in terms)
    elif isinstance(obj, bool):
        return "🔵 True" if obj else "🔴 False"
    elif hasattr(obj, '_repr_html_'):
        return str(obj._repr_html_())
    else:
        return ''.join([
            '<span onclick="$(\'input\', this).show().val('
            '$(\'span\', this).hide().text()).focus()[0].'
            'select(); document.execCommand(\'copy\')"><span>',
            html.escape(repr(obj)),
            '</span><input style="text-align: right; '
            'display: none; border: none; width: 100%; '
            'background: transparent;"></span>'])


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
                    time_to_sleep = last_call_time + period - now
                    if time_to_sleep > 0:
                        time.sleep(time_to_sleep)
                last_call_time = time.time()
                left_call_count = count
            left_call_count -= 1
            lock.release()

            return fn(*args, **kwargs)

        return wrapper

    return decorator


class DictObject(dict):
    def __getattr__(self, key: str) -> typing.Any:
        key = key.rstrip('_')
        if key in self:
            return self[key]
        else:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: typing.Any) -> None:
        self[key.rstrip('_')] = value

    def __delattr__(self, key: str) -> None:
        key = key.rstrip('_')
        if key in self:
            del self[key]
        else:
            raise AttributeError(key)

    def __dir__(self) -> typing.Iterable[str]:
        return [key for keys in (super().__dir__(), self.keys())
                for key in keys]

    def _repr_html_(self) -> str:
        return to_html(self)


class _Coinone(raw.Coinone):
    def _execute(self, path: str, **kwargs: typing.Any)\
            -> typing.Mapping[str, typing.Any]:
        json_opt = kwargs.get('_json_', {})
        json_opt['object_hook'] = DictObject
        kwargs['_json_'] = json_opt
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

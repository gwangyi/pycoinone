import json
import time
import base64
import hashlib
import hmac
import typing
import requests


def _default_nonce() -> int:
    return int(time.time() * 1000)


class Coinone:
    _base_url = 'https://api.coinone.co.kr/'
    _preferred_method = 'get'
    _preferred_payload = 'params'

    @staticmethod
    def _kwargs_to_payload(kwargs: typing.Mapping[str, typing.Any])\
            -> typing.Mapping[str, typing.Any]:
        payload = {k: v for k, v in kwargs.items()
                   if k[:1] != '_' and k[-1:] != '_'}
        return payload

    def __getattr__(self, key: str) -> '_APIEndpoint':
        return _APIEndpoint(self, '/' + key)

    def _execute(self, path: str, **kwargs: typing.Any)\
            -> typing.Mapping[str, typing.Any]:
        url = self._base_url + path.lstrip('/')
        headers = kwargs.get('_headers_', {})
        method = kwargs.get('_method_', self._preferred_method).upper()
        json_opt = kwargs.get('_json_', {})
        payload = self._kwargs_to_payload(kwargs)

        payload_type = kwargs.get('_payload_', self._preferred_payload)
        r = requests.request(method, url, headers=headers,
                             **{payload_type: payload})

        return typing.cast(typing.Mapping[str, typing.Any], r.json(**json_opt))


class CoinoneV1(Coinone):
    _base_url = 'https://api.coinone.co.kr/v1/'

    def __init__(self, access_token: str) -> None:
        super().__init__()
        self._access_token = access_token

    def _execute(self, path: str, **kwargs: typing.Any)\
            -> typing.Mapping[str, typing.Any]:
        if 'access_token' in kwargs:
            del kwargs['access_token']
        return super()._execute(path, access_token=self._access_token,
                                **kwargs)


class CoinoneV2(Coinone):
    _base_url = 'https://api.coinone.co.kr/v2/'
    _preferred_method = 'post'
    _preferred_payload = 'json'

    def __init__(self, access_token: str, secret_key: str,
                 nonce: typing.Callable[[], typing.Any] = _default_nonce)\
            -> None:
        super().__init__()
        self._nonce = nonce
        self._access_token = access_token
        self._secret_key = secret_key

    def _encode_payload(self, payload: typing.Mapping[str, typing.Any])\
            -> bytes:
        dumped_json = json.dumps(payload)
        return base64.b64encode(dumped_json.encode('utf-8'))

    def _signature(self, payload: bytes) -> str:
        signature = hmac.new(self._secret_key.upper().encode('ascii'),
                             payload,
                             hashlib.sha512)
        return signature.hexdigest()

    def _execute(self, path: str, **kwargs: typing.Any)\
            -> typing.Mapping[str, typing.Any]:
        headers: typing.Dict[str, str] = kwargs.get('_headers_', {})
        kwargs['access_token'] = self._access_token
        kwargs['nonce'] = self._nonce()
        payload = self._kwargs_to_payload(kwargs)

        encoded_payload: bytes = self._encode_payload(payload)

        headers.update({
            'X-COINONE-PAYLOAD': encoded_payload.decode('ascii'),
            'X-COINONE-SIGNATURE': self._signature(encoded_payload)
        })
        if '_headers_' in kwargs:
            del kwargs['_headers_']

        return super()._execute(path, _headers_=headers, **kwargs)


class _APIEndpoint:
    def __init__(self, session: Coinone, name: str) -> None:
        self._session = session
        self._name = name

    def __call__(self, **kwargs: typing.Any)\
            -> typing.Mapping[str, typing.Any]:
        return self._session._execute(self._name, **kwargs)

    def __getattr__(self, key: str) -> '_APIEndpoint':
        return _APIEndpoint(self._session, '/'.join((self._name, key)))

# PyCoinone

A Python wrapper for [Coinone][Coinone] API

Coinone API documentation can be obtain in [Coinone API Documentation][apidoc].

[Coinone]: https://coinone.co.kr
[apidoc]: https://doc.coinone.co.kr

## Install

Clone this repository and install with pip.

```bash
git clone https://github.com/gwangyi/pycoinone
cd pycoinone
pip install .
```

## Example

```python
from coinone.core import Coinone, CoinoneV1, CoinoneV2

api = Coinone()

print(api.orderbook(currency='btc'))  # http://api.coinone.co.kr/orderbook/

api = CoinoneV1(access_token="YOUR_ACCESS_TOKEN")

print(api.account.balance())  # https://api.coinone.co.kr/v1/account/balance/

api = CoinoneV2(access_token="YOUR_ACCESS_TOKEN",
                secret_key="YOUR_SECRET_KEY")

print(api.account.balance())  # https://api.coinone.co.kr/v2/account/balance/
```

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).

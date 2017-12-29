import enum


class Currency(str, enum.Enum):
    BTC = 'btc'
    BCH = 'bch'
    ETH = 'eth'
    ETC = 'etc'
    XRP = 'xrp'
    QTUM = 'qtum'
    IOTA = 'iota'
    LTC = 'ltc'
    BTG = 'btg'

    KRW = 'krw'


class OrderType(int, enum.Enum):
    Ask = 1
    Bid = 0
    Sell = 1
    Buy = 0

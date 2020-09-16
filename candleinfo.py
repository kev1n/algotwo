import oandapyV20.endpoints.instruments as instruments
from oandapyV20 import API

api = API(access_token = "cb3a119e20da9774b726411bd6fb2ea7-46b5e2129cc402d1c587e15d671f67c8")
def candlestickinfo(candlecount, granularity):
    parameters = {
    "count": candlecount,
    "granularity": granularity
    }

    info = instruments.InstrumentsCandles(instrument="EUR_USD", params=parameters)
    api.request(info)
    return info.response


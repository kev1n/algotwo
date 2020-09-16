import oandapyV20.endpoints.pricing as pricing
from oandapyV20 import API

api = API(access_token = "3f03c5e8deab57ba878beccfc33e6ee4-603b7ab6a7aa0f219f45bfd5005931e8")
accountid = '101-001-16126938-001'

def price():
    params = {"instruments": "EUR_USD"}
    price = pricing.PricingInfo(accountID=accountid, params=params)
    api.request(price)
    response = price.response

    bid = response['prices'][0]['bids'][0]['price']
    ask = response['prices'][0]['asks'][0]['price']
    return bid, ask



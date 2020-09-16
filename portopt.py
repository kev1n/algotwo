import oandapyV20.endpoints.positions as positions
from oandapyV20 import API

api = API(access_token = "9d7d7e9482fc2a6503873de241e6909b-7933db93f3e3e2079b5c32cdf234f496")
accountID= '101-001-16332577-001'

def openpositions():
    account_details = positions.OpenPositions(accountID= accountID)
    api.request(account_details)

    details = account_details.response

    return details

opened = openpositions()

for i in range(len(opened['positions'])):   
    if opened['positions'][i]['instrument'] == 'EUR_USD':
        if int(opened['positions'][i]['long']['units']) > 0:
            print(int(opened['positions'][i]['long']['units']))
        
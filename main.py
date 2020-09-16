from pricingstream import price
from portopt import openpositions
from candleinfo import candlestickinfo
from oandapyV20.contrib.requests import MarketOrderRequest
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
import oandapyV20
import json
from datetime import datetime
from pytz import timezone
import time
from candleinfo import candlestickinfo
import numpy as np
import tulipy as ti
from indicators import *

def main():
    api = API(access_token = "9d7d7e9482fc2a6503873de241e6909b-7933db93f3e3e2079b5c32cdf234f496")
    accountID= '101-001-16332577-001'
    listoftime = []

    longed = 0
    shorted = 0

    while True:
        candle = (candlestickinfo(1, 'M1'))['candles'][0]
        bid, ask = price()

        tz = timezone('US/Eastern')
        timenow = datetime.now(tz) 

        if candle['time'] not in listoftime:
            listoftime.append(candle['time'])
            if len(listoftime) > 1:
                emata = EMA('M1', 200)
                pk, pd = stoch('M1', 5, 3, 3)
                rsi = RSI('M1', 20)
                tplevel = 0.00035
                sllevel = 0.0005

                opened = openpositions()
                #Entry logic
                if float(bid) / float(ask) >= 0.99985:
                    if float(candle['mid']['o']) > float(emata):

                        #Buy when price is greater than ema 200
                        if not opened['positions']:
                            longed = 0
                        
                        if longed == 0:
                            if (pk[-2] < pd[-2]) and (pk[-1] > (pd[-1] + 3.5)) and rsi < 50:
                                if (float(pk[-2]) < 50 and float(pd[-2]) < 50) and (float(pd[-1]) < 50 and float(pk[-1]) < 50):
                                    #Plus 5 for sharp crossover
                                    longmktOrder = MarketOrderRequest(instrument="EUR_USD",
                                        units=420000,
                                        takeProfitOnFill=TakeProfitDetails(price= (float(candle['mid']['o']) * (1 + tplevel))).data,
                                        stopLossOnFill = StopLossDetails(price= (float(candle['mid']['o']) * (1 - sllevel))).data)

                                    r = orders.OrderCreate(accountID, data=longmktOrder.data)
                                    try:
                                        #create the OrderCreate request
                                        rv = api.request(r)
                                        print("Bought units at {} at time {}".format(ask, timenow))

                                        longed = 1
                                    except oandapyV20.exceptions.V20Error as err:
                                        print(r.status_code, err)

                    for i in range(len(opened['positions'])):   
                        if opened['positions'][i]['instrument'] == 'EUR_USD':
                            if int(opened['positions'][i]['long']['units']) > 0:
                                if rsi > 85:
                                    closelongmktOrder = MarketOrderRequest(instrument="EUR_USD", units=-420000)
                                    r = orders.OrderCreate(accountID, data=closelongmktOrder.data)

                                    try:
                                        # create the OrderCreate request
                                        rv = api.request(r)
                                        print("Sold off units at {} at time {}".format(bid, timenow))
                                        longed = 0
                                    except oandapyV20.exceptions.V20Error as err:
                                        print(r.status_code, err)

                    if float(candle['mid']['o']) < float(emata):
                        #Sell when price is less than ema 200
                        if not opened['positions']:
                            shorted = 0
                        
                        if shorted == 0:
                            if (pk[-2] > pd[-2]) and (pd[-1] > pk[-1] + 3.5) and rsi > 50:
                                if (float(pk[-2]) > 50 and float(pd[-2]) > 50) and (float(pd[-1]) > 50 and float(pk[-1]) > 50):
                                    #Plus 5 for sharp crossover
                                    shortmktOrder = MarketOrderRequest(instrument="EUR_USD",
                                        units= -420000,
                                        takeProfitOnFill=TakeProfitDetails(price= (float(candle['mid']['o']) * (1 - tplevel))).data,
                                        stopLossOnFill= StopLossDetails(price= (float(candle['mid']['o']) * (1 + sllevel))).data)
                                    r = orders.OrderCreate(accountID, data=shortmktOrder.data)
                                    try:
                                        # create the OrderCreate request
                                        rv = api.request(r)
                                        print("Shorted units at {} at time {}".format(bid, timenow))
                                        shorted = 1
                                    except oandapyV20.exceptions.V20Error as err:
                                        print(r.status_code, err)


                    for i in range(len(opened['positions'])):
                        if opened['positions'][i]['instrument'] == 'EUR_USD':
                            if int(opened['positions'][i]['short']['units']) < 0:
                                if rsi < 15:
                                    covershortmktOrder = MarketOrderRequest(instrument="EUR_USD", units=420000)
                                    r = orders.OrderCreate(accountID, data=covershortmktOrder.data)

                                    try:
                                        # create the OrderCreate request
                                        rv = api.request(r)
                                        print("Covered units at {} at time {}".format(ask, timenow))
                                        shorted = 0
                                    except oandapyV20.exceptions.V20Error as err:
                                        print(r.status_code, err)
                else:
                    print('Bid/Ask too wide for entry or exit')

#Execption handler:

while True:
    try:
        main()
    except Exception as e:
        print(e)
        print('Restarting!')
        time.sleep(40)
        continue



    







    

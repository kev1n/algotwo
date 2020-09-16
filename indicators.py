from candleinfo import candlestickinfo
import numpy as np
import tulipy as ti
#Indicators
def RSI(candlestickperiod, period):
    closeprices = []
    listoftime = []
    EMA = candlestickinfo(22, candlestickperiod)
    for i in range(len(EMA['candles'])):
        if EMA['candles'][i]['complete'] == True:
            if EMA['candles'][i]['time'] not in listoftime:
                closeprices.append(float(EMA['candles'][i]['mid']['c']))
                listoftime.append(EMA['candles'][i]['time'])
    closearray = np.array(closeprices)

    ta = ti.rsi(closearray, period = period)
    return ta

def EMA(candlestickperiod, period):
    closeprices = []
    listoftime = []
    EMA = candlestickinfo(600, candlestickperiod)
    for i in range(len(EMA['candles'])):
        if EMA['candles'][i]['complete'] == True:
            if EMA['candles'][i]['time'] not in listoftime:
                closeprices.append(float(EMA['candles'][i]['mid']['c']))
                listoftime.append(EMA['candles'][i]['time'])
    closearray = np.array(closeprices)

    ta = ti.ema(closearray, period = period)
    return round(ta[-1],5)


def stoch(candlestickperiod, one, two, three):
    closeprices = []
    lowprices = []
    highprices = []
    listoftime = []
    stoch = candlestickinfo(11, candlestickperiod)
    for i in range(len(stoch['candles'])):
        if stoch['candles'][i]['complete'] == True:
            if stoch['candles'][i]['time'] not in listoftime:
                closeprices.append(float(stoch['candles'][i]['mid']['c']))
                lowprices.append(float(stoch['candles'][i]['mid']['l']))
                highprices.append(float(stoch['candles'][i]['mid']['h']))
                listoftime.append(stoch['candles'][i]['time'])
    closearray = np.array(closeprices)
    lowarray = np.array(lowprices)
    higharray = np.array(highprices)

    stoch_k, stoch_d = ti.stoch(higharray, lowarray, closearray, one, two, three)
    print(stoch_k)
    print(stoch_d)
    return stoch_k, stoch_d

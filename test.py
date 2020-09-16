from candleinfo import candlestickinfo
import numpy as np
import tulipy as ti
#Indicators
def stoch(candlestickperiod, one, two, three):
    closeprices = []
    lowprices = []
    highprices = []
    listoftime = []
    stoch = candlestickinfo(50, candlestickperiod)
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
    print('StochK = {}'.format([stoch_k[-1], stoch_k[-2]]))
    print('StochD = {}'.format([stoch_d[-1], stoch_d[-2]]))

    return ([stoch_k[-1], stoch_k[-2]]), ([stoch_d[-1], stoch_d[-2]])
pk, pd = stoch('M1', 5, 3, 3)
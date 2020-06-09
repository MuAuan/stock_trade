import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import datetime as dt
from pandas_datareader import data
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL


def get_stock(stock,start,end):
    df = data.DataReader(stock, 'stooq',start)["Close"]
    df = df.iloc[::-1]
    return df[start:end]

def STOD(close, n):
    STOK = close.rolling(n).mean()
    return STOK

def calc_dff(dK,dD):
    dff= dK.copy()
    for j in range(len(dK)):
        dff[j]=100*(dK[j]-dD[j])/(abs(dK[j])+abs(dD[j])+1)
    return dff

stock0 = '4005' #sony6758 Jal 9201 三井住友フィナンシャル　8316 docomo9437 ana9202 日産7201 fasuto9983 8411	みずほ 4005	住友化 4553 東和薬品 9432 NTT
stock = stock0 + '.JP'
start = dt.date(2020,1,1)
end = dt.date(2020,6,5)
df = pd.DataFrame(get_stock(stock, start, end))
series = df['Close']
print(series)
bunseki = "series" #series" #cycle" #trend

cycle, trend = sm.tsa.filters.hpfilter(series, 144)
fig, ax = plt.subplots(3,1)
ax[0].plot(series)
ax[0].set_title('Close')
ax[1].plot(trend)
ax[1].set_title('Trend')
ax[2].plot(cycle)
ax[2].set_title('Deviation')
plt.savefig("./stock/{}/dix_close_{}_{}now{}.png".format(stock0,stock,bunseki,start))
plt.pause(1)

df['Close']=series  #series" #cycle" #trend

df['%5K'] = STOD(df['Close'], 5)
df['%25D'] = STOD(df['Close'], 25)
print(df[0:30])
print(df.tail())
dff=calc_dff(df['%5K'][25:],df['%25D'][25:])

fig, (ax1,ax2,ax3) = plt.subplots(3,1,figsize=(1.6180 * 12, 4*2))
ax1.plot(df['Close'][25:],label = "close")
ax2.plot(df['%5K'][25:],label = "%5K")
ax2.plot(df['%25D'][25:],label = "%25D")
ax3.plot(dff[:],label = "(%K-%D)/%K")
ax1.legend()
ax2.legend()
ax3.legend()
ax1.grid()
ax2.grid()
ax3.grid()
plt.savefig("./stock/{}/dix_close_%5K%25D_{}_{}now{}.png".format(stock0,stock,bunseki,start))
plt.pause(1)
plt.close()


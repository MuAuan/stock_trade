import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from pandas_datareader import data
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL

def get_stock(stock,start,end):
    df = data.DataReader(stock, 'stooq',start)["Close"]
    df = df.iloc[::-1]
    return df[start:end]

def get_high(stock,start,end):
    df = data.DataReader(stock, 'stooq',start)['High']
    df = df.iloc[::-1]
    return df[start:end]

def get_low(stock,start,end):
    df = data.DataReader(stock, 'stooq',start)['Low']
    df = df.iloc[::-1]
    return df[start:end]

def STOK(close, low, high, n): 
    STOK = ((close - low.rolling(n).min()) / (high.rolling(n).max() - low.rolling(n).min())) * 100
    return STOK

def STOD(close, low, high, n):
    STOK = ((close - low.rolling(n).min()) / (high.rolling(n).max() - low.rolling(n).min())) * 100
    STOD = STOK.rolling(3).mean()
    return STOD

def calc_dff(dK,dD):
    dff= dK.copy()
    for j in range(len(dK)):
        #print(j)
        if dK[j]-dD[j]>0:
            dff[j]=100*(dK[j]-dD[j])/(abs(dK[j])+1)
        else:
            dff[j]=100*(dK[j]-dD[j])/(100-abs(dK[j])+1)
    return dff

stock0 = '8411' #sony6758 Jal 9201 三井住友フィナンシャル　8316 docomo9437 ana9202 日産7201 fasuto9983 8411	みずほ 4005	住友化 4553 東和薬品 9432 NTT
stock = stock0 + '.JP'
start = dt.date(2020,1,1)
end = dt.date(2020,6,5)
df = pd.DataFrame(get_stock(stock, start, end))
series = df['Close']
print(series)
bunseki = "trend" #series" #cycle" #trend

cycle, trend = sm.tsa.filters.hpfilter(series, 144)
fig, ax = plt.subplots(3,1)
ax[0].plot(series)
ax[0].set_title('close')
ax[1].plot(trend)
ax[1].set_title('Trend')
ax[2].plot(cycle)
ax[2].set_title('Deviation')
plt.savefig("./stock/{}/close_%K%D_{}_{}now{}.png".format(stock0,stock,bunseki,start))
plt.pause(1)
#plt.close()
df['Close']=trend #series #cycle #trend

df['High'] = get_high(stock, start, end)
series = df['High']
cycle, trend = sm.tsa.filters.hpfilter(series, 144)
#fig, ax = plt.subplots(3,1)
ax[0].plot(series)
ax[0].set_title('High')
ax[1].plot(trend)
ax[1].set_title('Trend')
ax[2].plot(cycle)
ax[2].set_title('Deviation')
plt.savefig("./stock/{}/high_%K%D_{}_{}now{}.png".format(stock0,stock,bunseki,start))
plt.pause(1)
#plt.close()
df['High']=trend #series #cycle #trend

df['Low'] = get_low(stock, start, end)
series = df['Low']
cycle, trend = sm.tsa.filters.hpfilter(series, 144)
#fig, ax = plt.subplots(3,1)
ax[0].plot(series)
ax[0].set_title('Low')
ax[1].plot(trend)
ax[1].set_title('Trend')
ax[2].plot(cycle)
ax[2].set_title('Deviation')
plt.savefig("./stock/{}/All_%K%D_{}_{}now{}.png".format(stock0,stock,bunseki,start))
plt.pause(1)
plt.close()
df['Low']=trend #series #cycle #trend

df['%K'] = STOK(df['Close'], df['Low'], df['High'], 14)
df['%D'] = STOD(df['Close'], df['Low'], df['High'], 14)
print(df[0:30])
print(df.tail())
dff=calc_dff(df['%K'][16:],df['%D'][16:])

fig, (ax1,ax2,ax3) = plt.subplots(3,1,figsize=(1.6180 * 12, 4*2))
ax1.plot(df['Close'][16:],label = "close")
ax2.plot(df['%K'][16:],label = "%K")
ax2.plot(df['%D'][16:],label = "%D")
ax3.plot(dff[:],label = "(%K-%D)/%K")
ax1.legend()
ax2.legend()
ax3.legend()
ax1.grid()
ax2.grid()
ax3.grid()
plt.savefig("./stock/{}/close_stc_%K%D_{}_{}now{}.png".format(stock0,stock,bunseki,start))
plt.pause(1)
plt.close()

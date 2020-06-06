#http://www.andrewshamlet.net/2017/07/13/python-tutorial-stochastic-oscillator/
    
import pandas as pd
import numpy as np
from pandas_datareader import data as web
import matplotlib.pyplot as plt
#%matplotlib inline

import datetime as dt
from pandas_datareader import data
stocks = data.DataReader(name="GOOG",data_source="yahoo", start=dt.date(2000, 1, 1), end=dt.datetime.now())
print(stocks.head(3))

def get_stock(stock,start,end):
    return data.DataReader(name="GOOG",data_source="yahoo", start=start, end=end)["Close"]
#web.DataReader(selected_dropdown_value, data_source='yahoo',start=start, end=end)['Close']
#df = web.DataReader("BAC", "iex", start, end)
#df = web.DataReader("BAC", "quandl", start, end)

def get_high(stock,start,end):
    #return web.DataReader(stock,'google',start,end)['High']
    return data.DataReader(name="GOOG",data_source="yahoo", start=start, end=end)['High']

def get_low(stock,start,end):
    #return web.DataReader(stock,'google',start,end)['Low']
    return data.DataReader(name="GOOG",data_source="yahoo", start=start, end=end)['Low']

def STOK(close, low, high, n): 
    STOK = ((close - low.rolling(n).min()) / (high.rolling(n).max() - low.rolling(n).min())) * 100
    return STOK

def STOD(close, low, high, n):
    STOK = ((close - low.rolling(n).min()) / (high.rolling(n).max() - low.rolling(n).min())) * 100
    STOD = STOK.rolling(3).mean()
    return STOD

df = pd.DataFrame(get_stock('FB', dt.date(2016,1,1), dt.date(2016,12,31)))
df['High'] = get_high('FB', dt.date(2016,1,1), dt.date(2016,12,31))
df['Low'] = get_low('FB', dt.date(2016,1,1), dt.date(2016,12,31))
df['%K'] = STOK(df['Close'], df['Low'], df['High'], 14)
df['%D'] = STOD(df['Close'], df['Low'], df['High'], 14)
print(df[0:30])
print(df.tail())

fig, (ax1,ax2) = plt.subplots(2,1,figsize=(1.6180 * 4, 4*1))
#, figsize = (20, 5)
ax1.plot(df['Close'][16:],label = "close")
ax2.plot(df['%K'][16:],label = "%K")
ax2.plot(df['%D'][16:],label = "%D")
ax1.legend()
ax2.legend()
ax1.grid()
ax2.grid()
plt.savefig("./stock/stc_%K%D.png")
plt.show()

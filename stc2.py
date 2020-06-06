#http://www.andrewshamlet.net/2017/07/13/python-tutorial-stochastic-oscillator/
    
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from pandas_datareader import data

stocks1 = data.DataReader('6758.JP', 'stooq') #sony
print(stocks1.head(3))

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

stock = '9437.JP' #sony6758 Jal 9201 三井住友フィナンシャル　8316 docomo9437
start = dt.date(2020,1,1)
end = dt.date(2020,6,5)
df = pd.DataFrame(get_stock(stock, start, end))
df['High'] = get_high(stock, start, end)
df['Low'] = get_low(stock, start, end)
df['%K'] = STOK(df['Close'], df['Low'], df['High'], 14)
df['%D'] = STOD(df['Close'], df['Low'], df['High'], 14)
print(df[0:30])
print(df.tail())

fig, (ax1,ax2) = plt.subplots(2,1,figsize=(1.6180 * 8, 4*2))
ax1.plot(df['Close'][16:],label = "close")
ax2.plot(df['%K'][16:],label = "%K")
ax2.plot(df['%D'][16:],label = "%D")
ax1.legend()
ax2.legend()
ax1.grid()
ax2.grid()
plt.savefig("./stock/stc_%K%D_{}_now.png".format(stock))
plt.show()

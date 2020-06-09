import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime as dt
from pandas_datareader import data
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL

#dn = np.random.randint(2, size=100)*2-1
#gwalk = np.cumprod(np.exp(dn*0.01))*100


def get_stock(stock,start,end):
    df = data.DataReader(stock, 'stooq',start)["Close"]
    df = df.iloc[::-1]
    return df[start:end]

stock0 = '6758' #sony6758 Jal 9201 三井住友フィナンシャル　8316 docomo9437 ana9202 日産7201 fasuto9983 8411	みずほ 4005	住友化 4553 東和薬品 9432 NTT
stock = stock0 + '.JP'
bunseki = "series"
start = dt.date(2020,1,1)
end = dt.date(2020,6,5)
df = pd.DataFrame(get_stock(stock, start, end))
gwalk = df['Close'].values.tolist()
#gwalk = df['Close']
print(gwalk[0:3])

def EMA1(x, n):
    #k = 3.45*(n+1)
    a= 2/(n+1)
    return pd.Series(x).ewm(alpha=a).mean()

y12 = EMA1(gwalk, 12)
y26 = EMA1(gwalk, 26)
MACD = y12 -y26
signal = EMA1(MACD, 9)
hist_=MACD-signal
ind = np.arange(len(signal))

fig, ax = plt.subplots(2,1)
ax[0].plot(gwalk,label="gwalk")
ax[0].plot(y12,label="y12")
ax[0].plot(y26,label="y26")
ax[1].plot(MACD,label="MACD")
ax[1].plot(signal,label="signal")
ax[1].bar(ind,hist_)
ax[0].legend()
ax[1].legend()
ax[0].grid()
ax[1].grid()
plt.savefig("./stock/{}/ema_close_%5K%25D_{}_{}now{}.png".format(stock0,stock,bunseki,start))
plt.pause(1)
plt.close()
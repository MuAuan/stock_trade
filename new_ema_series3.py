import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import datetime as dt
from pandas_datareader import data
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL
import pandas_datareader.data as DataReader

def get_stock(stock,start,end):
    df = data.DataReader(stock, 'stooq',start)["Close"]
    df = df.iloc[::-1]
    return df[start:end]

from numba import jit
@jit(nopython=True)
def EMA3(x, n):
    alpha = 2/(n+1)
    y = np.empty_like(x)
    y[0] = x[0]
    for i in range(1,len(x)):
        y[i] = alpha*x[i] + (1-alpha)*y[i-1]
    return y

def EMA1(x, n):
    #k = 3.45*(n+1)
    a= 2/(n+1)
    return pd.Series(x).ewm(alpha=a).mean()

#stock0 = 'ZM' #sony6758 Jal 9201 三井住友フィナンシャル　8316 docomo9437 ana9202 日産7201 fasuto9983 8411	みずほ 4005	住友化 4553 東和薬品 9432 NTT  NTTデータ: 9613 'GOOG','AAPL','FB','AMZN', 'AAL' シマノ7309 'ZM'
stock0 = ['6758','9201','8316','9437','9202','7201','9983','8411','4005','4553','9432','9613','7309'] 
#stock0 = ['GOOG','AAPL','FB','AMZN', 'AAL','ZM']
for j in stock0:
    stock = j  + '.T' #6758.T for yahoo, .JP for stooq
    start = dt.date(2020,1,1)
    end = dt.date(2020,6,11)
    #df = pd.DataFrame(get_stock(stock, start, end))
    df=DataReader.get_data_yahoo("{}".format(stock),start,end)
    date_df=df['Close'].index.tolist()
    series = df['Close'].values.tolist()

    bunseki = "trend" #series" #cycle" #trend
    cycle, trend = sm.tsa.filters.hpfilter(series, 144)
    df['Close'] = trend
    series2 = df['Close'].values.tolist()
    #print(series2[len(series2)-10:len(series2)])

    df['Close']=series  #series" #cycle" #trend
    df['Close2']=series2
    df['y12'] = EMA1(df['Close2'], 12)
    df['y26'] =  EMA1(df['Close2'], 26)
    df['MACD'] = df['y12'] -df['y26']
    df['MACD2'] = df['Close2'] -df['y26']
    df['signal2'] = EMA1(df['MACD2'], 9)
    df['signal'] = EMA1(df['MACD'], 9)
    df['hist_']=df['MACD2']-df['signal2']
    date_df=df['Close'].index.tolist()
    print(df[len(series)-10:len(series)])

    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(1.6180 * 8, 4*2),dpi=200)
    ax1.plot(df['Close'],label="series")
    ax1.plot(df['Close2'],label="series2")
    ax1.plot(df['y12'],label="y12")
    ax1.plot(df['y26'],label="y26")
    ax2.plot(df['MACD2'],label="MACD2")
    #ax2.plot(df['MACD'],label="MACD")
    ax2.plot(df['signal2'],label="signal2")
    #ax2.plot(df['signal'],label="signal")
    ax2.bar(date_df,df['hist_'])
    ax1.set_title("{}".format(j))
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    #ax2.set_ylim(-5,20)
    plt.savefig("./stock/{}/{}_{}_{}_.png".format("stock0",j,bunseki,end))
    plt.pause(1)
    plt.close()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime as dt
from pandas_datareader import data
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL


def get_fx(stock,start,end):
    df = data.DataReader(stock, 'stooq',start)["Close"]
    df = df.iloc[::-1]
    return df[start:end]

bunseki = "trend"
start = dt.date(2020,1,1)
end = dt.date(2020,6,11)

import pandas_datareader.data as DataReader

#fx_list = ['ZAR=X','JPY=X', 'EUR=X', 'GBP=X', 'AUD=X']
fx_list = ['JPY=X']
for j in fx_list:
    stock0= j
    df0=DataReader.get_data_yahoo("{}".format("JPY=X"),start,end)
    #df1=DataReader.get_data_yahoo("{}".format(stock0),start,end) 
    df=df0 #/df1
    print(df0)
    #print(df1)
    print(df)

    series=df['Close']
    cycle, trend = sm.tsa.filters.hpfilter(series, 144)
    df['trend']=  trend

    def EMA1(x, n):
        #k = 3.45*(n+1)
        a= 2/(n+1)
        return pd.Series(x).ewm(alpha=a).mean()

    series2 = df['trend'].values.tolist()
    print(series2[len(series2)-10:len(series2)])

    df['Close']=series  #series" #cycle" #trend
    df['Close2']=series2
    df['y12'] = EMA1(df['Close2'], 12)
    df['y26'] =  EMA1(df['Close2'], 26)
    df['MACD'] = df['y12'] -df['y26']
    df['MACD2'] = df['Close2'] -df['y26'] #12
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
    ax1.set_title("{}/{}".format(stock0,"JPY"))
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    #ax2.set_ylim(-5,5)
    plt.savefig("./fx/{}_{}_{}_.png".format(stock0,"JPN=X",end))
    plt.pause(1)
    plt.close()
    
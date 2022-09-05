import backtrader as bt
import pandas as pd
import numpy as np
# from get_score import get_score_ch
from sqlalchemy import create_engine
import talib as ta
import datetime
import pandas as pd

def find_vcp(ticker, date):
    engine= create_engine('sqlite:///./././dataset/us/us_ticker_price_yf.db')
    df = pd.read_sql('{}'.format(ticker), engine)
    df.rename(columns={'hgih':'high'},inplace=True)
    df['chg_pct'] = ((df.close - df.open)/df.open)*80
    df['close'] = df['close'].apply(lambda x: round(x,3))
    df['VMA20'] = ta.SMA(df.volume, timeperiod=20)

    end_index = df[df.datetime == '{}'.format(date)].index.values[0] + 1
    start_index = end_index - 130

    df = df[start_index:end_index]
    df_length = len(df)
    df.index = range(df_length)

    # 关闭警告的设置方法
    pd.set_option('mode.chained_assignment', None)
    # 判断是不是前后5天的极值点
    df['extremum'] = 0
    for i in range(5,df_length):
        if df.close.iloc[i] == df.close.iloc[i-5:i+5].min() or df.close.iloc[i] == df.close.iloc[i-5:i+5].max() :
            df['extremum'].iloc[i] = 1

    index_arr = np.array(df[df.extremum == 1].index)
    price_arr = np.array(df[df.extremum == 1].close)

    while True:    
        min1_val = np.min(price_arr)
        min1_pos = np.argmin(price_arr)
        min1_ind = index_arr[min1_pos]
        max1_val = round(df.iloc[:min1_ind].max().values[0],3)

        if price_arr[min1_pos+1:].size == 0:
            print('{} is not vcp in {}'.format(ticker,date))
            break
        
        min2_val = np.min(price_arr[min1_pos+1:])
        min2_pos = np.argmin(price_arr[min1_pos+1:]) + min1_pos + 1
        min2_ind = index_arr[min2_pos]
        max2_val = round(df.iloc[min1_ind+1:min2_ind].max().values[0],3)

        if price_arr[min2_pos+1:].size == 0:
            print('{} is not vcp in {}'.format(ticker,date))
            break

        min3_val = np.min(price_arr[min2_pos+1:])
        min3_pos = np.argmin(price_arr[min2_pos+1:]) + min2_pos + 1
        min3_ind = index_arr[min3_pos]
        max3_val = round(df.iloc[min2_ind+1:min3_ind].max().values[0],3)

        dec1 = (max1_val - min1_val) / max1_val
        dec2 = (max2_val - min2_val) / max2_val
        dec3 = (max3_val - min3_val) / max3_val

        vol1 = df.iloc[min1_ind].VMA20
        vol2 = df.iloc[min2_ind].VMA20
        vol3 = df.iloc[min3_ind].VMA20

        if dec1>dec2>dec3>0 and vol1>vol2>vol3 and min3_ind>120:
            print('{} is vcp in {}'.format(ticker,date))
            break
        else:
            print('{} is not vcp in {}'.format(ticker,date))
            break

def find_vcp_fixed(ticker, date):
    engine= create_engine('sqlite:///./././dataset/us/us_ticker_price_yf.db')
    df = pd.read_sql('{}'.format(ticker), engine)
    df.rename(columns={'hgih':'high'},inplace=True)
    df['chg_pct'] = ((df.close - df.open)/df.open)*80
    df['close'] = df['close'].apply(lambda x: round(x,3))
    df['VMA20'] = ta.SMA(df.volume, timeperiod=20)

    end_index = df[df.datetime == '{}'.format(date)].index.values[0] + 1
    start_index = end_index - 130

    df = df[start_index:end_index]
    df_length = len(df)
    df.index = range(df_length)

    # 关闭警告的设置方法
    pd.set_option('mode.chained_assignment', None)
    # 判断是不是前后5天的极值点
    df['extremum'] = 0
    for i in range(7,df_length):
        if df.low.iloc[i] == df.low.iloc[i-7:i+7].min() :
            df['extremum'].iloc[i] = 1
        elif df.high.iloc[i] == df.high.iloc[i-7:i+7].max():
            df['extremum'].iloc[i] = 2
    df['extremum_val'] = 0
    for i in range(df_length):
        if df.iloc[i].extremum == 1:
            df.extremum_val.iloc[i] = round(df.iloc[i].low,3)
        elif df.iloc[i].extremum == 2:
            df.extremum_val.iloc[i] = round(df.iloc[i].high,3)

    index_arr = np.array(df.query('extremum != 0').index)
    price_arr = np.array(df[df.extremum_val != 0].extremum_val)

    while True:    
        min1_val = np.min(price_arr)
        min1_pos = np.argmin(price_arr)
        min1_ind = index_arr[min1_pos]
        max1_val = round(df.iloc[:min1_ind].max().values[0],3)

        if price_arr[min1_pos+1:].size == 0:
            print('{} is not vcp in {}'.format(ticker,date))
            break
        
        min2_val = np.min(price_arr[min1_pos+1:])
        min2_pos = np.argmin(price_arr[min1_pos+1:]) + min1_pos + 1
        min2_ind = index_arr[min2_pos]
        max2_val = round(df.iloc[min1_ind+1:min2_ind].max().values[0],3)

        if price_arr[min2_pos+1:].size == 0:
            print('{} is not vcp in {}'.format(ticker,date))
            break

        min3_val = np.min(price_arr[min2_pos+1:])
        min3_pos = np.argmin(price_arr[min2_pos+1:]) + min2_pos + 1
        min3_ind = index_arr[min3_pos]
        max3_val = round(df.iloc[min2_ind+1:min3_ind].max().values[0],3)

        dec1 = (max1_val - min1_val) / max1_val
        dec2 = (max2_val - min2_val) / max2_val
        dec3 = (max3_val - min3_val) / max3_val

        vol1 = df.iloc[min1_ind].VMA20
        vol2 = df.iloc[min2_ind].VMA20
        vol3 = df.iloc[min3_ind].VMA20

        if dec1 > dec2 > dec3 > 0 and min3_ind > 120:
            print('{} is vcp in {}'.format(ticker,date))
            print('dec1:{} dec2:{} dec3:{}'.format(dec1,dec2,dec3))
            print('vol1:{} vol2:{} vol3:{}'.format(vol1,vol2,vol3))
            date1 = df.iloc[min1_ind].datetime
            date2 = df.iloc[min2_ind].datetime
            date3 = df.iloc[min3_ind].datetime
            print('min1:{} min2:{} min3:{}'.format(date1,date2,date3) )
            print('min3_ind:{}'.format(min3_ind))
            break
        else:
            print('{} is not vcp in {}'.format(ticker,date))
            break

def find_vcp_test(ticker, date):
    engine= create_engine('sqlite:///./././dataset/us/us_ticker_price_yf.db')
    df = pd.read_sql('{}'.format(ticker), engine)
    df.rename(columns={'hgih':'high'},inplace=True)
    df['chg_pct'] = ((df.close - df.open)/df.open)*80
    df['close'] = df['close'].apply(lambda x: round(x,3))
    df['VMA20'] = ta.SMA(df.volume, timeperiod=20)

    end_index = df[df.datetime == '{}'.format(date)].index.values[0] + 1
    start_index = end_index - 130

    df = df[start_index:end_index]
    df_length = len(df)
    df.index = range(df_length)

    # 关闭警告的设置方法
    pd.set_option('mode.chained_assignment', None)
    # 判断是不是前后5天的极值点
    df['extremum'] = 0
    for i in range(8,df_length):
        if df.low.iloc[i] == df.low.iloc[i-8:i+8].min() :
            df['extremum'].iloc[i] = 1
        elif df.high.iloc[i] == df.high.iloc[i-7:i+7].max():
            df['extremum'].iloc[i] = 2
    df['extremum_val'] = 0
    for i in range(df_length):
        if df.iloc[i].extremum == 1:
            df.extremum_val.iloc[i] = round(df.iloc[i].low,3)
        elif df.iloc[i].extremum == 2:
            df.extremum_val.iloc[i] = round(df.iloc[i].high,3)

    index_arr = np.array(df.query('extremum != 0').index)
    price_arr = np.array(df[df.extremum_val != 0].extremum_val)

    while True:    
        min1_val = np.min(price_arr)
        min1_pos = np.argmin(price_arr)
        min1_ind = index_arr[min1_pos]
        max1_val = round(df.iloc[:min1_ind].max().values[0],3)

        if price_arr[min1_pos+1:].size == 0:
            print('{} is not vcp in {}'.format(ticker,date))
            break
        
        min2_val = np.min(price_arr[min1_pos+1:])
        min2_pos = np.argmin(price_arr[min1_pos+1:]) + min1_pos + 1
        min2_ind = index_arr[min2_pos]
        max2_val = round(df.iloc[min1_ind+1:min2_ind].max().values[0],3)

        if price_arr[min2_pos+1:].size == 0:
            print('{} is not vcp in {}'.format(ticker,date))
            break

        min3_val = np.min(price_arr[min2_pos+1:])
        min3_pos = np.argmin(price_arr[min2_pos+1:]) + min2_pos + 1
        min3_ind = index_arr[min3_pos]
        max3_val = round(df.iloc[min2_ind+1:min3_ind].max().values[0],3)

        dec1 = (max1_val - min1_val) / max1_val
        dec2 = (max2_val - min2_val) / max2_val
        dec3 = (max3_val - min3_val) / max3_val

        vol1 = df.iloc[min1_ind].VMA20
        vol2 = df.iloc[min2_ind].VMA20
        vol3 = df.iloc[min3_ind].VMA20

        if dec1 > max(dec2, dec3) > 0 and min3_ind > 110:
            print('{} is vcp in {}'.format(ticker,date))
            print('dec1:{} dec2:{} dec3:{}'.format(dec1,dec2,dec3))
            print('vol1:{} vol2:{} vol3:{}'.format(vol1,vol2,vol3))
            date1 = df.iloc[min1_ind].datetime
            date2 = df.iloc[min2_ind].datetime
            date3 = df.iloc[min3_ind].datetime
            print('min1:{} min2:{} min3:{}'.format(date1,date2,date3) )
            print('min3_ind:{}'.format(min3_ind))
            break
        else:
            print('{} is not vcp in {}'.format(ticker,date))
            print('dec1:{} dec2:{} dec3:{}'.format(dec1,dec2,dec3))
            print('vol1:{} vol2:{} vol3:{}'.format(vol1,vol2,vol3))
            date1 = df.iloc[min1_ind].datetime
            date2 = df.iloc[min2_ind].datetime
            date3 = df.iloc[min3_ind].datetime
            print('min1:{} min2:{} min3:{}'.format(date1,date2,date3) )
            print('min3_ind:{}'.format(min3_ind))
            break
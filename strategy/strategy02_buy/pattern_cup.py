import backtrader as bt
import pandas as pd
import numpy as np
# from get_score import get_score_ch
from sqlalchemy import create_engine
import talib as ta
import datetime
import pandas as pd

def get_cup_df(ticker_name, target_date, time_zone):
    # 关闭警告的设置方法
    pd.set_option('mode.chained_assignment', None)
    # 
    engine= create_engine('sqlite:///././dataset/us/us_ticker_seven_year_price.db')
    # engine= create_engine('sqlite:///././dataset/us/us_ticker_seven_year_price.db')
    df = pd.read_sql('{}'.format(ticker_name), engine)
    df['VMA20'] = ta.SMA(df.Volume, timeperiod=20)
    try:
        # set the zone
        target_index = df[df.datetime == target_date].index.values[0] + 1
        start_index = target_index - time_zone
        df = df[start_index : target_index]
        df.index = range(len(df))
        if df.empty != True:
            return df
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

def judge_cup(ticker_name, target_date):
    res_30 = find_cup(ticker_name, target_date, 20)
    res_60 = find_cup(ticker_name, target_date, 45)
    if res_30 == 204:
        # print('error trade date')
        return
    elif res_30 == 205 or res_60 == 205:
        # print('find cup error')
        return
    elif res_30 != 203 or res_60 !=203:
        if res_30 == 203:
            # print('{} not 30-day cup in {}'.format(ticker_name,target_date))
            pass
        else:
            print('{} migt be 30-day cup {} in {}.'.format(ticker_name, res_30, target_date))
            return 200
        if res_60 == 203:
            # print('{} not 60-day cup in {}'.format(ticker_name,target_date))
            pass
        else:
            print('{} migt be 60-day cup {} in {}.'.format(ticker_name, res_60, target_date))
            return 200
    else:
        # print('{} not cup in {}'.format(ticker_name, target_date))
        return 203

def find_cup(ticker_name, target_date, time_zone):
    if get_cup_df(ticker_name, target_date, time_zone).empty == True:
        return 204
    else:
        try:
            time_zone += 10
            window = get_cup_df(ticker_name, target_date, time_zone)
            price_max = window[10:].High.max()
            index_max = window[window.High == price_max].index.values[0]
            price_min = window[index_max:].Low.min()
            index_min = window[window.Low == price_min].index.values[0]
            tail = window.tail(3)
            # 判断交易量的缩放
            len_cut = len(tail[tail.Volume < tail.VMA20])
            # 判断最高价和最低价在0.15-0.5的范围内，并且前两周的价格上升
            if 0.5 > (price_max - price_min) / price_max > 0.15 and window.iloc[0].Close < window.iloc[20].Close and len_cut == 3:
                if window.tail(1).Close.values[0] <= (price_max - price_min)/3 + price_min:
                    # return 'low zone'
                    return 200
                elif window.tail(1).Close.values[0] >= price_max - (price_max - price_min)/3:
                    # return 'handle zone'
                    return 201
                elif price_max - (price_max - price_min)/3 > window.tail(1).Close.values[0] > (price_max - price_min)/3 + price_min:
                    # return 'cheat zone'
                    return 202
                else:           
                    return 203
            else:
                return 203
        except:
            return 205
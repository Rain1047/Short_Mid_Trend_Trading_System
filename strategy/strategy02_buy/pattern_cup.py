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
    engine= create_engine('sqlite:///././dataset/us/us_ticker_seven_year_price.db')
    df = pd.read_sql('{}'.format(ticker_name), engine)
    df['VMA20'] = ta.SMA(df.Volume, timeperiod=20)
    try:
        # set the zone
        target_index = df[df.datetime == target_date].index.values[0] + 1
        start_index = target_index - time_zone
        df = df[start_index : target_index]
        df.index = range(len(df))
        return df
    except:
        return

def judge_cup(ticker_name, target_date):
    if find_cup(ticker_name, target_date, 40) != None:
        print('{} migt be 60-day cup {} in {}.'.format(ticker_name, find_cup(ticker_name, target_date, 60), target_date))
        return True
    elif find_cup(ticker_name, target_date, 65) != None:
        print('{} migt be 60-day cup {} in {}.'.format(ticker_name, find_cup(ticker_name, target_date, 90),target_date))
        return True
    else:
        return False

def find_cup(ticker_name, target_date, time_zone):
    try:
        window = get_cup_df(ticker_name, target_date, time_zone+20)
        price_max = window[20:].High.max()
        index_max = window[window.High == price_max].index.values[0]
        price_min = window[index_max:].Low.min()
        index_min = window[window.Low == price_min].index.values[0]
        tail = window.tail(3)
        len_cut = len(tail[tail.Volume < tail.VMA20])
        if 0.5 > (price_max - price_min) / price_max > 0.15 and df.iloc[0].Close < window.iloc[20].Close:
            if window.tail(1).Close.values[0] <= (price_max - price_min)/3+ price_min and len_cut == 3:
                return 'low zone'
            elif window.tail(1).Close.values[0] >= price_max - (price_max - price_min)/3 and len_cut == 3:
                return 'handle zone'
            elif price_max - (price_max - price_min)/3 > window.tail(1).Close.values[0] > (price_max - price_min)/3+ price_min and len_cut == 3:
                return 'cheat zone'
            else:           
                return
        else:
            return
    except:
        return
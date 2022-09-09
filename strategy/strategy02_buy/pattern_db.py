import backtrader as bt
import pandas as pd
import numpy as np
# from get_score import get_score_ch
from sqlalchemy import create_engine
import talib as ta
import datetime
import pandas as pd

def get_db_df(ticker_name, ticker_date, time_zone, extrem_zone):
    engine= create_engine('sqlite:///./././dataset/us/us_ticker_seven_year_price.db')
    df = pd.read_sql('{}'.format(ticker_name), engine)
    df['VMA20'] = ta.SMA(df.Volume, timeperiod=20)
    try:
        end_index = df[df.datetime == '{}'.format(ticker_date)].index.values[0] + 1
        start_index = end_index - time_zone
        df = df[start_index:end_index]
        df.index = range(len(df))

        # 关闭警告的设置方法
        pd.set_option('mode.chained_assignment', None)

        df['extremum'] = 0
        df_length = len(df)
        for i in range(7,df_length):
            if df.Low.iloc[i] == df.Low.iloc[i-7:i+7].min() :
                df['extremum'].iloc[i] = -1
            elif df.High.iloc[i] == df.High.iloc[i-7:i+7].max():
                df['extremum'].iloc[i] = 1
        return df
    except:
        return

def find_db(ticker_name, target_date, time_zone, extrem_zone):
    try:
        df = get_db_df(ticker_name, target_date, time_zone, extrem_zone)
        extrem_index_list = df.query('extremum == 1 or extremum == -1').index.to_list()
        extrem_value_list = df.query('extremum == 1 or extremum == -1').extremum.to_list()
        if extrem_value_list[-3:] == [-1,1,-1] and df.iloc[extrem_index_list.iloc[-3]].Close * 1.05 > df.iloc[extrem_index_list.iloc[-1]].Close > df.iloc[extrem_index_list.iloc[-3]].Close * 0.95:
            print(df.iloc[extrem_index_list.iloc[-3]].datetime)
            print(df.iloc[extrem_index_list.iloc[-2]].datetime)
            print(df.iloc[extrem_index_list.iloc[-1]].datetime)
            return True
        else:
            return
    except:
        return


def judge_db(ticker_name, target_date):
    if find_db(ticker_name, target_date, 20, 5) == True:
        # print('{} might be double bottom in {}.'.format(ticker_name, target_date))
        return True
    elif find_db(ticker_name, target_date, 40, 10) == True:
        # print('{} might be double bottom in {}.'.format(ticker_name, target_date))
        return True
    elif find_db(ticker_name, target_date, 60, 15) == True:
        # print('{} might be double bottom in {}.'.format(ticker_name, target_date))
        return True
    else:
        # print('{} might be double bottom in {}.'.format(ticker_name, target_date))
        return False
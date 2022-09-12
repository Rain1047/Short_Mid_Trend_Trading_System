import backtrader as bt
import pandas as pd
import numpy as np
# from get_score import get_score_ch
from sqlalchemy import create_engine
import talib as ta
import datetime
import pandas as pd

def get_db_df(ticker_name, target_date, time_zone, extrem_zone):
    engine= create_engine('sqlite:///./././dataset/us/us_ticker_seven_year_price.db')
    df = pd.read_sql('{}'.format(ticker_name), engine)
    df['VMA20'] = ta.SMA(df.Volume, timeperiod=20)
    try:
        end_index = df[df.datetime == '{}'.format(target_date)].index.values[0] + 1
        start_index = end_index - time_zone
        df = df[start_index:end_index]
        df.index = range(len(df))

        # 关闭警告的设置方法
        pd.set_option('mode.chained_assignment', None)

        df['extremum'] = 0
        df_length = len(df)
        for i in range(extrem_zone,df_length):
            if df.Low.iloc[i] == df.Low.iloc[i-extrem_zone:i+extrem_zone].min() :
                df['extremum'].iloc[i] = -1
            elif df.High.iloc[i] == df.High.iloc[i-extrem_zone:i+extrem_zone].max():
                df['extremum'].iloc[i] = 1
        if df.empty != True:
            return df
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()


def find_db(ticker_name, target_date, time_zone, extrem_zone):
    if get_db_df(ticker_name, target_date, time_zone, extrem_zone).empty == True:
        return 304
    try:
        df = get_db_df(ticker_name, target_date, time_zone, extrem_zone)
        extrem_index_list = df.query('extremum == 1 or extremum == -1').index.to_list()
        extrem_value_list = df.query('extremum == 1 or extremum == -1').extremum.to_list()
        # 最后为极低，极高，极低
        # 两个极低之间不超过0.05
        # 低得低点和极高点，超过0.05
        dec = (df.iloc[extrem_index_list[-2]].Close - min(df.iloc[extrem_index_list[-1]].Close, df.iloc[extrem_index_list[-3]].Close)) / df.iloc[extrem_index_list[-2]].Close
        if extrem_value_list[-3:] == [-1,1,-1] and df.iloc[extrem_index_list[-3]].Close * 1.05 > df.iloc[extrem_index_list[-1]].Close > df.iloc[extrem_index_list[-3]].Close * 0.95 and dec >= 0.05:
            # print(df.iloc[extrem_index_list.iloc[-3]].datetime)
            # print(df.iloc[extrem_index_list.iloc[-2]].datetime)
            # print(df.iloc[extrem_index_list.iloc[-1]].datetime)
            return 300
        else:
            return 303
    except:
        return 305


def judge_db(ticker_name, target_date):
    res_20 = find_db(ticker_name, target_date, 20, 5)
    res_40 = find_db(ticker_name, target_date, 40, 10)
    res_60 = find_db(ticker_name, target_date, 60, 15)
    if res_20 == 304:
        # print('{} might be double bottom in {}.'.format(ticker_name, target_date))
        return 304
    elif res_20 == 305:
        # print('error find db')
        return 305
    elif res_20 == 300 or res_40 == 300 or res_60 == 300:
        if res_20 == 300:
            print('{} might be double bottom in {}.'.format(ticker_name, target_date))
            return 300
        elif find_db(ticker_name, target_date, 40, 10) == 300:
            print('{} might be double bottom in {}.'.format(ticker_name, target_date))
            return 300
        elif find_db(ticker_name, target_date, 60, 15) == 300:
            print('{} might be double bottom in {}.'.format(ticker_name, target_date))
            return 300
    # print('{} might be double bottom in {}.'.format(ticker_name, target_date))
    else:
        # print('not double bottom')
        return
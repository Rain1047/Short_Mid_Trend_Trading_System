import backtrader as bt
import pandas as pd
import numpy as np
# from get_score import get_score_ch
from sqlalchemy import create_engine
import talib as ta
import datetime
import pandas as pd

# 
def get_vcp_df(ticker_name, ticker_date, time_zone, extrem_zone):
    engine= create_engine('sqlite:///./././dataset/us/us_ticker_seven_year_price.db')
    df = pd.read_sql('{}'.format(ticker_name), engine)
    df['Close'] = df['Close'].apply(lambda x: round(x,3))
    df['VMA20'] = ta.SMA(df.Volume, timeperiod=20)
    try:
        end_index = df[df.datetime == '{}'.format(ticker_date)].index.values[0] + 1
        start_index = end_index - time_zone
        df = df[start_index:end_index]
        df.index = range(len(df))

        # 关闭警告的设置方法
        pd.set_option('mode.chained_assignment', None)
        # 判断是不是前后5天的极值点
        df['extremum'] = 0
        for i in range(extrem_zone,len(df)):
            if df.Close.iloc[i] == df.Close.iloc[i-extrem_zone:i+extrem_zone].min() or df.Close.iloc[i] == df.Close.iloc[i-5:i+5].max() :
                df['extremum'].iloc[i] = 1
        df['extremum_val'] = 0
        for i in range(len(df)):
            if df.iloc[i].extremum == 1:
                df.extremum_val.iloc[i] = round(df.iloc[i].Low,3)
            elif df.iloc[i].extremum == 2:
                df.extremum_val.iloc[i] = round(df.iloc[i].High,3)
        return df
    except:
        return

# judge vcp
def judge_vcp(ticker_name, target_date):
    # 200天
    if find_vcp(ticker_name, target_date, 140, 12, 3)  == -1:
        print('not trade day')
        return -1
    elif find_vcp(ticker_name, target_date, 140, 12, 3) == True:
        print('{} might be 3 vcp in {}.'.format(ticker_name, target_date))
        return True
    elif find_vcp(ticker_name, target_date, 140, 8, 3) == True:
        print('{} might be 3 vcp in {}.'.format(ticker_name, target_date))
        return True
    else:
        # print('{} is not vcp in {}.'.format(ticker_name, target_date))
        return False


# find vcp
def find_vcp(ticker_name, target_date, time_zone, extrem_zone, vcp_count):
    if vcp_count == 3:
        try:
            df = get_vcp_df(ticker_name, target_date, time_zone, extrem_zone)
            index_arr = np.array(df.query('extremum != 0').index)
            price_arr = np.array(df[df.extremum_val != 0].extremum_val)

            while True:    
                min1_val = np.min(price_arr)
                min1_pos = np.argmin(price_arr)
                min1_ind = index_arr[min1_pos]
                max1_val = round(df.iloc[:min1_ind].max().values[0],3)

                if price_arr[min1_pos+1:].size == 0:
                    # print('{} is not vcp in {}'.format(ticker_name,target_date))
                    return False
                
                min2_val = np.min(price_arr[min1_pos+1:])
                min2_pos = np.argmin(price_arr[min1_pos+1:]) + min1_pos + 1
                min2_ind = index_arr[min2_pos]
                max2_val = round(df.iloc[min1_ind+1:min2_ind].max().values[0],3)

                if price_arr[min2_pos+1:].size == 0:
                    # print('{} is not vcp in {}'.format(ticker_name, target_date))
                    return False

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

                if max(dec1, dec2) > dec3 and max(vol1, vol2) > vol3 and min3_ind > time_zone * 0.67 and [max(max2_val, max3_val, df.tail(1).Close) - min(max2_val, max3_val, df.tail(1).Close)] / max(max2_val, max3_val, df.tail(1).Close) < 0.15:
                    # print('{} is vcp in {}'.format(ticker_name,target_date))
                    # print('dec1:{} dec2:{} dec3:{}'.format(dec1,dec2,dec3))
                    # print('vol1:{} vol2:{} vol3:{}'.format(vol1,vol2,vol3))
                    # date1 = df.iloc[min1_ind].datetime
                    # date2 = df.iloc[min2_ind].datetime
                    # date3 = df.iloc[min3_ind].datetime
                    # print('min1:{} min2:{} min3:{}'.format(date1,date2,date3) )
                    # print('min3_ind:{}'.format(min3_ind))
                    # break
                    return True
                else:
                    print('{} is not vcp in {}'.format(ticker_name, target_date))
                    print('dec1:{} dec2:{} dec3:{}'.format(dec1,dec2,dec3))
                    print('vol1:{} vol2:{} vol3:{}'.format(vol1,vol2,vol3))
                    date1 = df.iloc[min1_ind].datetime
                    date2 = df.iloc[min2_ind].datetime
                    date3 = df.iloc[min3_ind].datetime
                    print('min1:{} min2:{} min3:{}'.format(date1,date2,date3) )
                    print('min3_ind:{}'.format(min3_ind))
                    break
                    return False
        except:
            return -1

    if vcp_count == 2:
        try:
            df = get_vcp_df(ticker_name, target_date, time_zone, extrem_zone)
            index_arr = np.array(df.query('extremum != 0').index)
            price_arr = np.array(df[df.extremum_val != 0].extremum_val)

            while True:    
                min1_val = np.min(price_arr)
                min1_pos = np.argmin(price_arr)
                min1_ind = index_arr[min1_pos]
                max1_val = round(df.iloc[:min1_ind].max().values[0],3)

                if price_arr[min1_pos+1:].size == 0:
                    # print('{} is not vcp in {}'.format(ticker_name,target_date))
                    return False
                
                min2_val = np.min(price_arr[min1_pos+1:])
                min2_pos = np.argmin(price_arr[min1_pos+1:]) + min1_pos + 1
                min2_ind = index_arr[min2_pos]
                max2_val = round(df.iloc[min1_ind+1:min2_ind].max().values[0],3)

                if price_arr[min2_pos+1:].size == 0:
                    # print('{} is not vcp in {}'.format(ticker_name, target_date))
                    return False

                dec1 = (max1_val - min1_val) / max1_val
                dec2 = (max2_val - min2_val) / max2_val

                vol1 = df.iloc[min1_ind].VMA20
                vol2 = df.iloc[min2_ind].VMA20

                if dec1 > dec2 and vol1 > vol2:
                    print('{} is vcp in {}'.format(ticker_name,target_date))
                    # print('dec1:{} dec2:{}'.format(dec1,dec2))
                    # print('vol1:{} vol2:{}'.format(vol1,vol2))
                    date1 = df.iloc[min1_ind].datetime
                    date2 = df.iloc[min2_ind].datetime
                    print('min1:{} min2:{}'.format(date1,date2) )
                    # break
                    return True
                else:
                    # print('{} is not vcp in {}'.format(ticker_name, target_date))
                    # print('dec1:{} dec2:{}'.format(dec1,dec2))
                    # print('vol1:{} vol2:{}'.format(vol1,vol2))
                    date1 = df.iloc[min1_ind].datetime
                    date2 = df.iloc[min2_ind].datetime
                    print('min1:{} min2:{}'.format(date1,date2))
                    # break
                    return False
        except:
            return -1
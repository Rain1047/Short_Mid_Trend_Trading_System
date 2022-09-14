import backtrader as bt
import pandas as pd
import numpy as np
# from get_score import get_score_ch
from sqlalchemy import create_engine
import talib as ta
import datetime
import pandas as pd

def judge_vcp(df):
    df.index = range(len(df))
    df_length = len(df)
    # 获取Volume MA
    df['VMA20'] = ta.SMA(df.volume, timeperiod=20)
    # 判断是不是10天内的极值点
    df['extremum'] = 0
    for i in range(5,df_length):
        # or df.close.loc[i] == df.close.loc[i-5:i+5].max() 
        if df.close.loc[i] == df.close.loc[i-5:i+5].min():
            df['extremum'].loc[i] = 1
            
    minimum_index = np.array(df[df['extremum']==1].index)
    minimum_value = np.array(df[df['extremum']==1].close)

    # Main
    # 140约等于200天
    df = df[9834:9984]
    df.index = range(len(df))
    df_length = len(df)

    # find the min1
    min1_val = np.min(minimum_value)
    min1_pos = np.argmin(minimum_value)
    min1_ind = minimum_index[min1_pos]
    # find the max1
    max1_val = df.iloc[:min1_ind].close.max()

    # min2
    min2_val = np.min(minimum_value[min1_pos+1:])
    min2_pos = np.argmin(minimum_value[min1_pos+1:]) + min1_pos + 1
    min2_ind = minimum_index[min2_pos]
    # max2
    max2_val = df.iloc[min1_ind:min2_ind].close.max()

    # min3
    min3_val = np.min(minimum_value[min2_pos+1:])
    min3_pos = np.argmin(minimum_value[min2_pos+1:]) + min2_pos + 1
    min3_ind = minimum_index[min3_pos]
    # max3
    max3_val = df.iloc[min2_ind:min3_ind].close.max()

    # volume
    vol1 = df.iloc[min1_ind].VMA20
    vol2 = df.iloc[min2_ind].VMA20
    vol3 = df.iloc[min3_ind].VMA20

    # decent rate    
    dec1 = (max1_val - min1_val) / max1_val
    dec2 = (max2_val - min2_val) / max2_val
    dec3 = (max3_val - min3_val) / max3_val

    # Select
    if vol1 > vol2 > vol3 and dec1 > dec2 >dec3 and max2_val*1.05 > max3_val:
        return 1
        print('ticker is vcp')
    else:
        return 0
        print('not vcp pattern')
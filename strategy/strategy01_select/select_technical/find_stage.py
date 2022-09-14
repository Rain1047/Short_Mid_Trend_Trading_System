import backtrader as bt
import pandas as pd
import numpy as np
# from get_score import get_score_ch
from sqlalchemy import create_engine
import talib as ta
import datetime
import pandas as pd

def find_scond_stage(ticker, inputdate):
    engine= create_engine('sqlite:///./././dataset/us/us_ticker_price_yf.db')
    df = pd.read_sql('{}'.format(ticker), engine)
    df.rename(columns={'hgih':'high'},inplace=True)
    df['chg_pct'] = ((df.close - df.open)/df.open)*100
    df['close'] = df['close'].apply(lambda x: round(x,3))
    df['VMA20'] = ta.SMA(df.volume, timeperiod=20)
    df['VMA50'] = ta.SMA(df.volume, timeperiod=50)


    # 关闭警告的设置方法
    pd.set_option('mode.chained_assignment', None)
    df['vol_diff'] = 0
    df['rate_diff'] = 0

    targetindex = df[df.datetime == '{}'.format(inputdate)].index.values[0]
    startindex = targetindex - 50
    temp = df[startindex: targetindex]
    increase_volume = round(temp[temp.chg_pct > 0].volume.mean(),3)
    decrease_volume = round(temp[temp.chg_pct < 0].volume.mean(),3)
    increase_rate = round(temp.query('chg_pct > 0 and volume > VMA20').datetime.count() / temp.query('chg_pct > 0').datetime.count(),3)
    decrease_rate = round(temp.query('chg_pct < 0 and volume > VMA20').datetime.count() / temp.query('chg_pct < 0').datetime.count(),5)
    # df['vol_diff'].iloc[targetindex] = round((increase_volume - decrease_volume) / 1000,0)
    # df['rate_diff'].iloc[targetindex]  = round((increase_rate - decrease_rate)*1000,3)
    # for i in range(50,df_leng
    vol_diff = round((increase_volume - decrease_volume) / 1000,0)
    rate_diff = round((increase_rate - decrease_rate)*1000,3)

    temp['factor'] = round(temp.volume / temp.VMA20, 3)
    increase_rate_fac = temp.query('chg_pct > 0 and volume > VMA20').factor.sum() / temp.query('chg_pct > 0').factor.count()
    decrease_rate_fac = temp.query('chg_pct < 0 and volume > VMA20').factor.sum() / temp.query('chg_pct < 0').factor.count()
    rate_diff_fac = round((increase_rate_fac - decrease_rate_fac)*1000 ,3)

    # 高成交量下的增长天数和下降天数
    increase_date_count = temp.query('volume > VMA50 and chg_pct > 0').datetime.count()
    decrease_date_count = temp.query('volume > VMA50 and chg_pct < 0').datetime.count()
    date_diff =  increase_date_count - decrease_date_count

    print('date: {}, date diff: {}, rate diff: {}, rate diff with factor:{}'.format(inputdate, date_diff, rate_diff, rate_diff_fac))
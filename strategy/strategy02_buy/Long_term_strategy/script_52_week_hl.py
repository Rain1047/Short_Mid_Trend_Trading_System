import backtrader as bt
import pandas as pd
import numpy as np
# from get_score import get_score_ch
from sqlalchemy import create_engine
import talib as ta
import datetime
import pandas as pd

# pro = ts.pro_api(token=token)
engine= create_engine('sqlite:///../../dataset/us/us_ticker_price_yf.db')
def select_price(ticker_list):
    total = pd.DataFrame()
    for ticker in ticker_list:
        # 引入数据
        df = pd.read_sql(ticker, engine)
        # 我们需要大概两年的数据
        df = df.tail(500)
        df.rename(columns={'hgih':'high'},inplace=True)
        df['close'] = df['close'].apply(lambda x: round(x,3))
        # 处理数据
        ## Moving Average
        timeperiods = [10,20,50,150,200]
        vol_timeperiods = [20,50]
        for period in timeperiods:
            df['MA{}'.format(period)] = ta.SMA(df.close)
        for period in vol_timeperiods:
            df['VMA{}'.format(period)] = ta.SMA(df.volume)

        ## 52 week high and low
        one_year_high = df.tail(365).close.max()
        one_year_low = df.tail(365).close.min()
        ## 60 day high and low
        sixty_day_high = df.tail(60).close.max()
        sixty_day_low = df.tail(60).close.min()
        # 创建单个ticker的row
        temp = pd.DataFrame()
        temp['symbol'] = 'symbol'
        temp['datetime'] = df.tail(1).datetime
        temp.symbol = ticker

        # origin editon
        # condition1: close > MA50 > MA150 > MA200 
        # condition2: close > max(52week_low * 1.25, 52week_high*0.75)
        # condition3: rs
        temp['con1'] = 0
        temp['con2'] = 0
        if df.iloc[0].close > df.iloc[0].MA50 > df.iloc[0].MA150 > df.iloc[0].MA200:
            temp['con1'] = 1
        # improve editon
        # condition1: close>20 MA10>MA50 MA20>MA200 MA50>MA200
        # condition2: 
        if df.iloc[0].MA150 > df.iloc[0].MA20 and df.iloc[0].MA10 > df.iloc[0].MA50 and df.iloc[0].MA20 > df.iloc[0].MA200 and df.iloc[0].MA50 > df.iloc[0].MA200:
            temp['con2'] = 1

        # 52 week high and low
        # 注：为1就是好的
        temp['52-week-zone'] = 0
        temp['60-day-zone'] = 0
        if df.iloc[-1].close >= one_year_high * 0.75 and df.iloc[-1].close >= one_year_low * 1.25:
            temp['52-week-zone'] = 3
        elif df.iloc[-1].close >= one_year_high * 0.75:
            temp['52-week-zone'] = 2
        elif df.iloc[-1].close >= one_year_low * 1.25: 
            temp['52-week-zone'] = 1
        
        if df.iloc[-1].close > sixty_day_high * 0.9 and df.iloc[-1].close > sixty_day_low * 1.1:
            temp['60-day-zone'] = 3
        elif df.iloc[-1].close >= sixty_day_low * 1.1:
            temp['60-day-zone'] = 2
        elif df.iloc[-1].close >= sixty_day_high * 0.9: 
            temp['60-day-zone'] = 1
 
        total = pd.concat([total, temp])
    total.index = range(len(total))
    return total
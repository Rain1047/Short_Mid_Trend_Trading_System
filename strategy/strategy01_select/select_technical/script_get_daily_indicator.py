
import pandas as pd
import yfinance as yf 
from sqlalchemy import create_engine
import talib as ta
import tushare as ts
ticker_engine = create_engine('sqlite:///./././dataset/us/us_ticker_list_with_name.db')
price_engine = create_engine('sqlite:///./././dataset/us/us_ticker_seven_year_price.db')
indicator_engine = create_engine('sqlite:///./././dataset/us/us_ticker_with_indicator.db')

def get_daily_indicator(target_date):
    name_df = pd.read_sql('TOTAL', con=ticker_engine)
    ticker_list = name_df.Symbol.to_list()
    total_df = pd.DataFrame()
    for ticker in ticker_list:
        try:
            df = pd.read_sql('{}'.format(ticker), con=price_engine)
            df.dropna(inplace=True)
            df = df.iloc[:df[df.datetime == '{}'.format(target_date)].index.values[0] + 1]
            if len(df) > 200:
                df['ticker'] = ticker
                timeperiod = [10,20,50,150,200]
                # MA
                for period in timeperiod:
                    df['MA{}'.format(period)] = ta.SMA(df.Close, timeperiod=period)
                vol_timeperiod = [20,50]
                for period in vol_timeperiod:
                    df['VMA{}'.format(period)] = ta.SMA(df.Volume, timeperiod=period)
                # high&low
                df['year_high'] = df.tail(252).High.max()
                df['year_low'] = df.tail(252).Low.min()
                # rs
                df = df.tail(252)
                df['rs'] = round((df.tail(1).MA20.values[0] - df.head(1).MA20.values[0]) / df.head(1).MA20.values[0],3)
                df = df.tail(1)
                total_df = pd.concat([total_df, df],ignore_index=True)
            else:
                continue
        except:
            continue
    total_df.to_sql('{}'.format(target_date),if_exists='replace',index=None,con=indicator_engine)
    print('Done')
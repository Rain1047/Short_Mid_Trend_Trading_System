# Pandas
import pandas as pd
import talib as ta
import numpy as np
# from get_score import get_score_ch
from sqlalchemy import create_engine

def get_sell_point_us(ticker):
    engine= create_engine('sqlite:///../single_ticker_price/us/us_ticker_price_yf.db')
    df = pd.read_sql('{}'.format(ticker), engine)
    df.rename(columns={'hgih':'high'},inplace=True)
    df['chg_pct'] = ((df.close - df.open)/df.open)*100
    # df[df.chg_pct > 0].chg_pct.describe()

    timeperiods_close = [10, 20, 50, 150, 200]
    timeperiods_volume = [20, 50]
    # Get Close Price MA
    # for i in timeperiods_close:
    #     df['MA {}'.format(i)] = ta.SMA(df.close, timeperiod = i)

    # Get Volume MA
    for i in timeperiods_volume:
        df['VMA{}'.format(i)] = ta.SMA(df.volume, timeperiod=i)

    get_profit_list = []
    len_df = len(df)
    for i in range(361,len_df):
        max_ = df.loc[i-360:i].high.max()
        if max_*0.95 < df.loc[i].close:
            if df.loc[i].volume < df.loc[i].VMA50 * 1:
                get_profit_list.append(df.loc[i].datetime)

    get_profit_df = pd.DataFrame({
        'datetime':get_profit_list,
    })
    get_profit_df = get_profit_df[360:]
    get_profit_df.to_csv('{}_profit_datetime.csv'.format(ticker))
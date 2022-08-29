# Pandas
import pandas as pd
import talib as ta
import numpy as np
from sqlalchemy import create_engine
from get_score import get_score_ch
engine= create_engine('sqlite:///../../dataset/us/us_ticker_price_yf.db')

ticker = input("input ticker symbol:")
# 我们选取近十年的
df = pd.read_sql('{}'.format(ticker),engine)
df.rename(columns={'hgih':'high'},inplace=True)
score_df = get_score_ch(df)
score_df.to_csv('{}_score.csv'.format(ticker),index=False)

df = pd.read_csv('{}_score.csv')
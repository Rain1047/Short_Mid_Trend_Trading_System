
# 数据库
import sqlite3
from sqlalchemy import create_engine
# 数据处理
import pandas as pd
import talib as ta
import numpy as np
# 股票API
import tushare as ts 
import baostock as bs
import yfinance as yf
# 时间
from datetime import datetime
# 多线程
from concurrent.futures import ThreadPoolExecutor
# Token
ts_token = '28ce867873a056747209a2ef0ff53d98ed850903fd954417ac69553b'
# Database Relative Address
database_ch = 'sqlite:///dataset/database_ch.db'
database_us = ''
database_cp = ''

# pro = ts.set_token(token=ts_token)
# df = ts.pro_bar(ts_code='000001.SZ', adj='qfq')
# print(df)
# engine_ch = create_engine(database_ch)
# df = pd.read_sql('ticker_list', con=engine_ch)
# print(df)
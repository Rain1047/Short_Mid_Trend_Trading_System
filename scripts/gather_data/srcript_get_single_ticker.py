# 存入数据库
## Write into SQL
import sqlite3
from datetime import datetime
# Pandas
import pandas as pd
import talib as ta
import numpy as np
# stock api
import baostock as bs
import yfinance as yf
# from get_score import get_score_ch
from sqlalchemy import create_engine

def get_single_ticker_ch():
    # ----------------------------------------# 
    #                get SSE
    # ----------------------------------------#
    # create engine
    engine= create_engine('sqlite:///../../dataset/ch/ticker_symbol_ch.db')
    df = pd.read_sql('SSE',engine)
    # change the symbol code
    df.symbol = 'sh.' + df.symbol.astype(str)
    ticker_list = df.symbol.to_list()

    # connect database
    database = "./single_ticker_price/ch/ch_ticker_price.db"
    conn = sqlite3.connect(database)
    print('connect success!')

    #### 登陆系统 ####
    lg = bs.login()

    for ticker in ticker_list:
        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus("{}".format(ticker),
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            frequency="d", adjustflag="3")

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        #### 结果集输出到csv文件 ####   
        # result.to_csv("D:\\history_A_stock_k_data.csv", index=False)

        #### 结果输出到SQL ####
        try:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE {}(date, code, open, high, low, close, volume, amount, pctChg)'.format(ticker))
            conn.commit()
            print("Table ceate successful!")
        except:
            print("Table name already exists")
        
        # 写入（如果没有就写入，否则建立资料表）
        try:
            result.to_sql('{}'.format(ticker), conn, if_exists='replace',index=False)
        except:
            print('df already exits')

    #### 登出系统 ####
    bs.logout()

    # ----------------------------------------# 
    #                get SZSE
    # ----------------------------------------#
    engine= create_engine('sqlite:///ticker_symbol_ch.db')
    df = pd.read_sql('SZSE',engine)
    df.symbol = 'sz.' + df.symbol.astype(str)
    ticker_list = df.symbol.to_list()
    ## connect database
    database = "./single_ticker_price/ch/ch_ticker_price.db"
    conn = sqlite3.connect(database)
    print('connect success!')

    #### 登陆系统 ####
    lg = bs.login()

    for ticker in ticker_list:
        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus("{}".format(ticker),
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            frequency="d", adjustflag="3")

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        #### 结果集输出到csv文件 ####   
        # result.to_csv("D:\\history_A_stock_k_data.csv", index=False)


        #### 结果输出到SQL ####
        try:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE {}(date, code, open, high, low, close, volume, amount, pctChg)'.format(ticker))
            conn.commit()
            print("Table ceate successful!")
        except:
            print("Table name already exists")
        
        # 写入（如果没有就写入，否则建立资料表）
        try:
            result.to_sql('{}'.format(ticker), conn, if_exists='replace',index=False)
        except:
            print('df already exits')

    #### 登出系统 ####
    bs.logout()

def get_single_ticker_us(ticker_list):
    engine= create_engine('sqlite:///ticker_symbol_us.db')
    df = pd.read_sql('TOTAL',engine)
    ticker_list = df.Ticker.to_list()

    ## connect database
    database = "./single_ticker_price/us/us_ticker_price_yf.db"
    conn = sqlite3.connect(database)
    print('connect success!')

    for ticker in ticker_list:
        try:
            data = yf.download("{}".format(ticker))
            data['datetime'] = data.index.values
            data['datetime'] = data['datetime'].apply(lambda x:x.strftime('%Y-%m-%d'))
            data.rename(columns = {'Open':'open', 'High':'high','Low':'low','Close':'close','Volume':'volume'}, inplace = True)
            
            # create the table(only once)
            try:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE {}(datetime, open, high, low, close, volume)'.format(ticker))
                conn.commit()
                print("Table ceate successful!")
            except:
                print("{} already exists".format(ticker))

            # 写入（如果没有就写入，否则建立资料表）
            try:
                data.to_sql('{}'.format(ticker), conn, if_exists='replace', index=False)
            except:
                print('df already exits')
        except:
            print('{} is wrong'.format(ticker))
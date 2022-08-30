# 获取股票的ticker列表，以及其分类和交易所类型
import tushare as ts
from pyfinviz.screener import Screener
import pandas as pd
# 中国股票列表
# 返回格式为dataframe
def get_tikcer_list_ch():
    ts.set_token('28ce867873a056747209a2ef0ff53d98ed850903fd954417ac69553b')
    pro = ts.pro_api()
    sse_ticker = pro.query('stock_basic', exchange='SSE', list_status='L', fields='ts_code,symbol,name,area,industry')
    szse_ticker = pro.query('stock_basic', exchange='SZSE', list_status='L', fields='ts_code,symbol,name,area,industry')
    bse_ticker = pro.query('stock_basic', exchange='BSE', list_status='L', fields='ts_code,symbol,name,area,industry')
    return sse_ticker, szse_ticker,bse_ticker

# import pyfinviz
def get_ticker_list_us_nasdaq():
    df_nasdaq = pd.DataFrame()   
    # with no params (default screener table)
    screener = Screener()
    # NASDAQ Technology
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.TECHNOLOGY]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 30)])

    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])

    df_nasdaq['Ticker'] = df.Ticker
    df_nasdaq['Sector'] = 'Technology'
    df_nasdaq['Exchange'] = 'NASDAQ' 
    # df_nasdaq.index = range(len(df_nasdaq))
    
    # NASDAQ Energy
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.ENERGY]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 5)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Energy'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    # NASDAQ Basic_Materials
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.BASIC_MATERIALS]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 5)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Basic_Materials'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    # NASDAQ Financial
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.FINANCIAL]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 65)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Financial'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    # NASDAQ Healthcare
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.HEALTHCARE]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 65)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Healthcare'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    # NASDAQ Communication_Services
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.COMMUNICATION_SERVICES]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 11)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Communication_Services'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    # NASDAQ Consumer_Cyclical
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.CONSUMER_CYCLICAL]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 16)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Consumer_Cyclical'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    # NASDAQ Consumer_Defensive
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.CONSUMER_DEFENSIVE]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 8)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Consumer_Defensive'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    # NASDAQ Industrials
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.INDUSTRIALS]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 16)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Industrials'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    # NASDAQ Real_Estate
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.REAL_ESTATE]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 5)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Real_Estate'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    # NASDAQ Utilities
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.UTILITIES]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 4)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Utilities'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    # NASDAQ Energy
    options = [Screener.ExchangeOption.NASDAQ, Screener.SectorOption.ENERGY]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 5)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Energy'
    df_['Exchange'] = 'NASDAQ'

    df_nasdaq = df_nasdaq.append(df_)
    df_nasdaq.index = range(len(df_nasdaq))

    return df_nasdaq

def get_ticker_list_us_nyse():
    df_nyse = pd.DataFrame()
    # NYSE Energy
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.ENERGY]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 11)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Energy'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    # NYSE Financial
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.FINANCIAL]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 110)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Financial'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    # NYSE Healthcare
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.HEALTHCARE]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 8)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Healthcare'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    # NYSE Industrials
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.INDUSTRIALS]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 18)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Industrials'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    # NYSE Real_Estate
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.REAL_ESTATE]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 12)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Real_Estate'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    # NYSE Technology
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.TECHNOLOGY]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 12)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Technology'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    # NYSE Utilities
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.UTILITIES]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 12)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Utilities'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    # NYSE Basic_Materials
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.BASIC_MATERIALS]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 10)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Basic_Materials'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    # NYSE Communication_Services
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.COMMUNICATION_SERVICES]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 6)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Communication_Services'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    # NYSE Consumer_Defensive
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.CONSUMER_DEFENSIVE]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 7)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Consumer_Defensive'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    # NYSE Consumer_Cyclical
    options = [Screener.ExchangeOption.NYSE, Screener.SectorOption.CONSUMER_CYCLICAL]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                        pages=[x for x in range(1, 15)])
    # get screener
    len_ = len(screener.data_frames)
    for i in range(len_):
        if i == 0:
            df = screener.data_frames[i]
        elif i!=1 and screener.data_frames[i].shape[0] > 1:
            df = df.append(screener.data_frames[i])
    # create temp list
    df_ = pd.DataFrame()
    df_['Ticker'] = df.Ticker
    df_['Sector'] = 'Consumer_Cyclical'
    df_['Exchange'] = 'NYSE'

    df_nyse = df_nyse.append(df_)
    df_nyse.index = range(len(df_nyse))

    return df_nyse
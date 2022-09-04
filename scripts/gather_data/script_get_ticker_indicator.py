import pandas as pd
import yfinance as yf 
from sqlalchemy import create_engine
import talib as ta

# now
def get_ticker_indicator():
    engine = create_engine('sqlite:///././dataset/us/us_ticker_list_with_name.db')
    # Get ticker string
    ticker_df = pd.read_sql('TOTAL',con=engine)
    ticker_list = ticker_df.Symbol.to_list()
    ticker_str = ''
    for ticker in ticker_list:
        ticker_str = ticker_str + str(ticker) + " "

    data = yf.download(
        tickers = ticker_str,
        period = '2y',
        interval = '1d',
        group_by = 'ticker',
        auto_adjust = True,
        treads = True
    )
    error_list = []
    total = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'datetime', 'MA10', 'MA20',
        'MA50', 'MA150', 'MA200', 'VMA20', 'VMA50', 'symbol'])
    for ticker in ticker_list:
        try:
            # print('{} start'.format(ticker))
            df = data['{}'.format(ticker)]
            df.dropna(inplace=True)
            df['symbol'] = ticker
            df['datetime'] = df.index
            timeperiod = [10,20,50,150,200]
            for period in timeperiod:
                df['MA{}'.format(period)] = ta.SMA(df.Close, timeperiod=period)
            vol_timeperiod = [20,50]
            for period in vol_timeperiod:
                df['VMA{}'.format(period)] = ta.SMA(df.Volume, timeperiod=period)
            target = df.tail(1)
            total = pd.concat([total, target],ignore_index=True)
        except:
            print('{} error'.format(ticker))
            error_list.append(ticker)

    total.dropna(inplace=True)
    total.index = range(len(total))

    engine = create_engine('sqlite:///././dataset/us/us_ticker_with_indicator.db')
    datetime = total.datetime[1]
    datetime = str(datetime)
    datetime = datetime[:10]
    total.to_sql('{}'.format(datetime), con=engine)


def get_ticker_indicator_his(start_date, end_date):
    engine = create_engine('sqlite:///././dataset/us/us_ticker_list_with_name.db')
    # Get ticker string
    ticker_df = pd.read_sql('TOTAL',con=engine)
    ticker_list = ticker_df.Symbol.to_list()
    ticker_str = ''
    for ticker in ticker_list:
        ticker_str = ticker_str + str(ticker) + " "
    data = yf.download(
        tickers=ticker_str, 
        start=start_date,
        end=end_date,
        interval = '1d',
        group_by = 'ticker',
        auto_adjust = True,
        treads = True
        )
    error_list = []
    total = pd.DataFrame()
    for ticker in ticker_list:
        try:
            # print('{} start'.format(ticker))
            df = data['{}'.format(ticker)]
            df.dropna(inplace=True)
            df['symbol'] = ticker
            df['datetime'] = df.index
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
            target = df.tail(1)
            total = pd.concat([total, target],ignore_index=True)
        except:
            print('{} error'.format(ticker))
            error_list.append(ticker)

    total.dropna(inplace=True)
    total.index = range(len(total))
    try:
        engine = create_engine('sqlite:///././dataset/us/us_ticker_with_indicator.db')
        # datetime = total.datetime[1]
        # datetime = str(datetime)
        # datetime = datetime[:10]
        total.to_sql('{}'.format(end_date),if_exists="replace",index=None, con=engine)
    except:
        print('error occur')
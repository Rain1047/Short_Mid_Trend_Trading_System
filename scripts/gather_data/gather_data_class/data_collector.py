from libraries import *

class data_collector():
    def __init__(self) -> None:
        pass
    
    global get_ticker_list
    def get_ticker_list(market='us'):
        if market == 'us':
            engine = create_engine(database_us)
            df = pd.read_sql('ticker_list', con=engine)
            ticker_list = df.Ticker.to_list()
            print('get us ticker list')
            return ticker_list 
        if market == 'ch':
            engine = create_engine(database_ch)
            df = pd.read_sql('ticker_list', con=engine)
            ticker_list = df.ts_code.to_list()
            print('get ch ticker list')
            return ticker_list 
        if market == 'cp':
            s = Screener()
            data = s.get_screeners('all_cryptocurrencies_us', count=250)
            # data is in the quotes key
            dicts = data['all_cryptocurrencies_us']['quotes']
            ticker_list = [d['symbol'] for d in dicts]
            return ticker_list 
    
    global gather_ticker_ch
    def gather_ticker_ch(ticker):
        df = ts.pro_bar(ts_code=ticker, adj='qfq')
        engine_ch = create_engine(database_ch)
        df.to_sql(ticker, con=engine_ch, if_exists='replace', index=None)
        print('{} ok'.format(ticker))


    global connect_database
    def connect_database(market):
        if market == 'us':
            database = ''
            return database 
        if market == 'ch':
            database = ''
            return database 
        if market == 'cp':
            database = ''
            return database 



    def gather_fundamental(self, market):
        if market == 'us':
            pass 
        elif market == 'ch':
            pass 
        pass

    def gather_history(self, market):
        if market == 'us':
            ticker_list = get_ticker_list(market) 
            ticker_str = ''
            try:
                for ticker in ticker_list:
                    ticker_str = ticker_str + str(ticker) + ' '
                print(ticker_str)
                data = yf.download(
                        tickers = ticker_str,
                        period = '5y',
                        interval = '1d',
                        group_by = 'ticker' ,
                        threads = True
                    )
                engine = create_engine(database_us)
                for ticker in tqdm(ticker_list):
                    df = data[ticker]
                    df['Datatime'] = df.index
                    df.to_sql(ticker, con=engine, if_exists='replace',index=None)
            except:
                print('need vpn or proxy')
        elif market == 'ch':
            ticker_list = get_ticker_list(market) 
            with ThreadPoolExecutor(8) as executor:
                executor.map(gather_ticker_ch, ticker_list)
        elif market == 'cp':
            # tickers
            ticker_list = get_ticker_list(market) 
            ticker_str = ''
            for ticker in ticker_list:
                ticker_str = ticker_str + ticker + ' '
            # use threads
            data = yf.download(
                tickers = ticker_str, 
                period = '2y', 
                interval = '1d', 
                group_by = 'ticker', 
                threads = True,
            )
            engine = create_engine(database_cp)
            pd.set_option('mode.chained_assignment', None)
            for ticker in tqdm(ticker_list):
                df = data[ticker]
                df['Datetime'] = df.index
                df.to_sql(ticker, con=engine, if_exists='replace',index=None)

dc = data_collector()
dc.gather_history('cp')

# ticker_list = get_ticker_list(market='cp')
# print(ticker_list)
# # print(1)
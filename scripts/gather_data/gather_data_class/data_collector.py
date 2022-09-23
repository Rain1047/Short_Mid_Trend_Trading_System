from libraries import *

class data_collector():
    def __init__(self) -> None:
        pass
    
    global get_ticker_list
    def get_ticker_list(market='ch'):
        if market == 'us':
            ticker_list = []
            print('us')
            return ticker_list 
        if market == 'ch':
            engine_ch = create_engine(database_ch)
            df = pd.read_sql('ticker_list', con=engine_ch)
            ticker_list = df.ts_code.to_list()
            print('ch')
            return ticker_list 
        if market == 'cp':
            ticker_list = []
            return ticker_list 
    
    global gather_ticker
    def gather_ticker(ticker):
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
            pass 
        elif market == 'ch':
            ticker_list = get_ticker_list(market)
            with ThreadPoolExecutor(8) as executor:
                executor.map(gather_ticker, ticker_list)
        elif market == 'cp':
            pass
        pass

dc = data_collector()
dc.gather_history('ch')
# ticker_list = get_ticker_list(market='us')

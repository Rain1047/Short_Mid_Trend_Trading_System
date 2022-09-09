# from pattern_vcp import find_vcp as jv
# from find_pattern import find_vcp_fixed as jvfix
# from find_pattern import find_vcp_test as jv
from sqlalchemy import create_engine
import pandas as pd
from pattern_vcp import judge_vcp as jv
from pattern_cup import judge_cup as jv
from pattern_db import judge_db as jd
from script_find_pattern import find_pattern as fb

# Get datetime list 
def get_date_list(start_date):
    engine= create_engine('sqlite:///./././dataset/us/us_ticker_price_yf.db')
    df = pd.read_sql('AAPL',con=engine)
    d_index = df[df.datetime == start_date].index.values[0]
    df = df[d_index:]
    date_list = df.datetime.to_list()
    return date_list

def get_data_list():
    engine = create_engine('sqlite:///./././dataset/us/us_ticker_list_with_name.db')
    df = pd.read_sql('TOTAL',con=engine)
    ticker_list = df.Symbol.to_list()
    return ticker_list



# ticker_df = pd.read_csv(r'strategy\strategy01_select\select_technical\selected_ticker_list_08_28.csv')
# ticker_list = ticker_df.symbol.to_list()


# -------------------------------------# 
# Check one tickers in multipul days
# -------------------------------------# 
# ticker = 'INTC'
# date_list = get_date_list(start_date ='2019-10-02')
# for i in range(0, len(date_list), 2):
#     jv(ticker, date_list[i])


# -------------------------------------# 
# Check multipul tickers in multipul days
# -------------------------------------# 
# for ticker in ticker_list:
#     for i in range(0, len(date_list),2):
#         jvfix('{}'.format(ticker), date_list[i])

# -------------------------------------# 
# Check multipul tickers in one day
# -------------------------------------# 

# for ticker in ticker_list:
#     try:
#         # for i in range(0, len(date_list),2):
#         jvfix('{}'.format(ticker), '2022-07-08')
#     except:
#         print('error')


jv('INTC','2019-10-02')
# jv('INTC','2020-01-09')
# jv('GOOG','2019-07-23')
# jv('GOOG','2019-07-30')
# jv('GOOG','2018-06-13')
# jv('GOOG','2018-06-13')
# jv('AMD','2020-07-08')

# jv('LTC','2022-07-12')

# jv('BRT','2022-07-12')

# jv('TSLA','2021-08-24')

# jv('AMD','2020-07-08')

# jv('LTC','2022-07-12')

# jv('BRT','2022-07-12')

# jv('TSLA','2021-08-24')

# jv('NVDA','2021-10-19')
# jd('AMD', '2021-05-21')
# jv('AMD', '2021-08-04')
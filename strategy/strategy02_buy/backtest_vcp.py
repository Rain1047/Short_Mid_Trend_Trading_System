from find_pattern import find_vcp as fv
from find_pattern import find_vcp_fixed as fvfix
from find_pattern import find_vcp_test as fvt
from sqlalchemy import create_engine
import pandas as pd

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
ticker = 'AMD'
date_list = get_date_list(start_date ='2022-04-27')
for i in range(0, len(date_list), 3):
    fvfix('{}'.format(ticker), date_list[i])
    # print(1)


# -------------------------------------# 
# Check multipul tickers in multipul days
# -------------------------------------# 
# for ticker in ticker_list:
#     for i in range(0, len(date_list),2):
#         fvfix('{}'.format(ticker), date_list[i])

# -------------------------------------# 
# Check multipul tickers in one day
# -------------------------------------# 

# for ticker in ticker_list:
#     try:
#         # for i in range(0, len(date_list),2):
#         fvfix('{}'.format(ticker), '2022-07-08')
#     except:
#         print('error')
# # fv('INTC','2019-10-25')
# fv('INTC','2020-01-09')
# fv('GOOG','2019-07-23')
# fv('GOOG','2019-07-30')
# fv('GOOG','2018-06-13')
# fv('GOOG','2018-06-13')
fvt('AMD','2020-07-08')

fvt('LTC','2022-07-12')

fvt('BRT','2022-07-12')
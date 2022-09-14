from find_stage import find_scond_stage as f2s
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

# # check the ticker
# for i in range(0,len(datetime),3):
#     date = datetime[i]
#     # fv('BABA',date)
#     # f2s('AAPL',date)
#     f2s('AMZN',date)

date_list = get_date_list(start_date ='2019-11-11')
ticker = 'AMZN'
for date in date_list:
    f2s('{}'.format(ticker), date)
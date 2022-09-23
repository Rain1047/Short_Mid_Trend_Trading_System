import pandas as pd
from sqlalchemy import create_engine
import tushare as ts
from strategy_downtrend import downtrend_strategy as ds
#获取富时中国50指数
# df = pro.index_global(ts_code='SPX', start_date='20000201', end_date='20220913')

# get ticker list 
# ticker_engine = create_engine('sqlite:///./././dataset/us/us_ticker_list_with_name.db')
ticker_engine = create_engine('sqlite:///./././dataset/us/ticker_symbol_us.db')
ticker_df = pd.read_sql('TOTAL', con=ticker_engine)
# ticker_list = ticker_df.Symbol.to_list()
ticker_list = ticker_df.Ticker.to_list()

downtrend_list =[
                # ['2022-01-03', '2022-06-21'],
                ['2020-02-20', '2022-03-23'],
                ['2018-10-03', '2018-12-26'],
                ['2007-10-08', '2009-03-09'],
                ['2000-08-28', '2003-03-10']]

downtrend_engine = create_engine('sqlite:///strategy\strategy01_select\select_downtrend\downtrend_select_result_2nd.db')

res = pd.DataFrame()
for i in range(len(downtrend_list)):
    for ticker in ticker_list:
        try:
            temp = ds('{}'.format(ticker), downtrend_list[i][0], downtrend_list[i][1])
            res = pd.concat([res, temp],ignore_index=True)
        except:
            continue
    res.to_sql('{}'.format(downtrend_list[i][0]), con = downtrend_engine, if_exists='replace', index=None)

import pandas as pd
from sqlalchemy import create_engine
price_engine = create_engine('sqlite:///./././dataset/us/us_ticker_seven_year_price.db')
ticker_engine = create_engine('sqlite:///./././dataset/us/us_ticker_list_with_name.db')

def downtrend_strategy(ticker_name, start_date, end_date):
    # get spx last time
    spx = pd.read_csv(r'strategy\strategy01_select\select_downtrend\SPX.csv')
    spx.trade_date = spx.trade_date.apply(lambda x: str(x))
    start_index = spx[spx.trade_date == start_date].index.values[0]
    end_index = spx[spx.trade_date == end_date].index.values[0]
    last_count = abs(start_index - end_index)
    try:
        ticker_df = pd.read_sql('{}'.format(ticker_name),con=price_engine)
    except:
        print('{} not in the list'.format(ticker_name))
    
    try:
        # 初始价格
        start_price = ticker_df[ticker_df.datetime == start_date].Close.values[0]
        # 初始价格时的index
        tstart_index = ticker_df[ticker_df.datetime == start_date].index.values[0]
        # 下降中的最低价
        lowest_price = min(ticker_df[tstart_index:tstart_index+int(last_count*1.33)].Low)
        # 最低价时的index
        lowest_index = ticker_df[ticker_df.Low == lowest_price].index.values[0]
        # 下降率
        decline_rate = round((start_price - lowest_price) / start_price, 3)
        # 下降时间
        tlast_count = abs(lowest_index - tstart_index)
        # 更新df的范围，起始点为最低价
        ticker_df = ticker_df[lowest_index:]
    except:
        print('{} not trade time'.format(start_date))

    # 获取到达原价75%时的index和价格
    if ticker_df[ticker_df.Close >= start_price * 0.75].empty != True:
        rev_h_index = ticker_df[ticker_df.Close >= start_price * 0.75].index.values[0]
        rev_h_price = ticker_df[ticker_df.Close >= start_price * 0.75].Close.values[0]
    else:
        rev_h_index = 9999
        rev_h_price = 9999
    # 获取到达最低价125%时的index
    if ticker_df[ticker_df.Close >= lowest_price * 1.25].empty != True:
        rev_l_index = ticker_df[ticker_df.Close >= lowest_price * 1.25].index.values[0]
        rev_l_price = ticker_df[ticker_df.Close >= lowest_price * 1.25].Close.values[0]
    else: 
        rev_l_index = 9999
        rev_l_price = 9999
    # 分别计算到达的时间
    rev_h_count = abs(rev_h_index - lowest_index)
    rev_l_count = abs(rev_l_index - lowest_index)
    # 进场点（用于计算收益，取小的index）
    # get enter_point和enter_prices
    if rev_h_index == rev_l_index == 9999:
        print('can not continue')
        return pd.DataFrame()
    elif rev_h_index == 9999:
        rev_h_count = 9999
        rev_l_count = abs(rev_l_index - lowest_index)
        enter_point = rev_l_count
        enter_price = rev_l_price
    elif rev_l_index == 9999:
        rev_l_count = 9999
        rev_h_count = abs(rev_h_index - lowest_index)
        enter_point = rev_h_count
        enter_price = rev_h_price
    else:
        # 分别计算到达的时间
        rev_h_count = abs(rev_h_index - lowest_index)
        rev_l_count = abs(rev_l_index - lowest_index)
        if rev_l_count < rev_h_count:
            enter_point = rev_l_count
            enter_price = rev_l_price
        else:
            enter_point = rev_h_count
            enter_price = rev_h_price

    # 更新df范围，起始点变为进场点
    ticker_df = ticker_df[enter_point:]
    max_30 = max(ticker_df[:int(30/7*5)].Close)
    max_60 = max(ticker_df[:int(60/7*5)].Close)
    max_90 = max(ticker_df[:int(90/7*5)].Close)
    max_180 = max(ticker_df[:int(180/7*5)].Close)
    profit_30 = (max_30 - enter_price) / enter_price
    profit_60 = (max_60 - enter_price) / enter_price
    profit_90 = (max_90 - enter_price) / enter_price
    profit_180 = (max_180 - enter_price) / enter_price
    # res = pd.DataFrame()
    temp = pd.DataFrame([[ticker_name,decline_rate,tlast_count,rev_h_count, rev_l_count, profit_30,profit_60,profit_90,profit_180]],columns=['ticker','dec_rate','dec_time','rec_h_time','rec_l_time','pft_30','pft_60','pft_90','pft_180'])
    # res = pd.concat([res,temp],ignore_index=True)
    print('{} success'.format(ticker_name))
    return temp
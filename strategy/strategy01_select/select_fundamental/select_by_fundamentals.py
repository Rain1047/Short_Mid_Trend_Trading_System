import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def get_name_list(target_add):
    name_engine = create_engine('sqlite:///./././dataset/us/us_ticker_list_with_name.db')
    target_engine = create_engine(target_add)
    name_df = pd.read_sql('TOTAL',con=name_engine)
    name_list = name_df.Symbol.to_list()
    # Clean the data
    # 我们需要将没有这个数据的ticker从我们的list中去除，以提高下面程序运行的速度
    for ticker in name_list:
        try:
            test_df = pd.read_sql('{}-Quarter'.format(ticker),con=target_engine)
        except:
            name_list.remove(ticker)
    return name_list

def get_selected_df(selected_df,quarter_df,ticker,targetdate):
    try:   
        if len(quarter_df) < targetdate + 7:
            print('{} data not enough'.format(ticker))
            return selected_df
        quarter_df['growth_rate'] = 0
        for i in range(len(quarter_df)-4):
            quarter_df.growth_rate.iloc[i] = (quarter_df.eps.iloc[i] - quarter_df.eps.iloc[i+4]) / quarter_df.eps.iloc[i+4]
        # fix the growth rate
        quarter_df['fixed_growth_rate'] = 0
        for i in range(len(quarter_df)-1):
            quarter_df.fixed_growth_rate.iloc[i] = (quarter_df.growth_rate.iloc[i] + quarter_df.growth_rate.iloc[i+1]) / 2 
        # pick the ticker
        if quarter_df.iloc[targetdate].growth_rate > quarter_df.iloc[targetdate+1].growth_rate > quarter_df.iloc[targetdate+2].growth_rate > 0.2 or quarter_df.iloc[targetdate].growth_rate > 1:
            g1 = quarter_df.iloc[targetdate].growth_rate
            g2 = quarter_df.iloc[targetdate+1].growth_rate
            g3 = quarter_df.iloc[targetdate+2].growth_rate
            temp = pd.DataFrame([[ticker,g1,g2,g3]],columns=['ticker','g1','g2','g3'])
            selected_df = pd.concat([selected_df,temp])
            print('{} selected'.format(ticker))
            return selected_df
        elif quarter_df.iloc[targetdate].fixed_growth_rate > quarter_df.iloc[targetdate+1].fixed_growth_rate > quarter_df.iloc[targetdate+2].fixed_growth_rate > 0.2 or quarter_df.iloc[targetdate].fixed_growth_rate > 1:
            g1 = quarter_df.iloc[targetdate].fixed_growth_rate
            g2 = quarter_df.iloc[targetdate+1].fixed_growth_rate
            g3 = quarter_df.iloc[targetdate+2].fixed_growth_rate
            temp = pd.DataFrame([[ticker,g1,g2,g3]],columns=['ticker','g1','g2','g3'])
            selected_df = pd.concat([selected_df,temp])
            print('{} selected'.format(ticker))
            return selected_df
        else:
            print('{} not selected'.format(ticker))
            return selected_df
    except:
        print('{} not exsit'.format(ticker))
        return selected_df

def clean_df(selected_df):
    selected_df.replace([np.inf, -np.inf], np.nan,inplace=True)
    selected_df.dropna(axis=0, inplace=True)
    selected_df.index = range(len(selected_df))
    return selected_df

# when target date equals to 0, means getting the lastest 
# when target date equals to 1, means getting the last quarter
def select_by_eps_fixed(targetdate = 0):
    # ignore the warnings
    pd.set_option('mode.chained_assignment', None)
    # get the name list 
    target_add = 'sqlite:///./././dataset/us/us_ticker_quarter.db'
    name_list = get_name_list(target_add)
    print('name list got')
    # create the engine
    quarter_engine = create_engine(target_add)
    # create the select dataframe
    selected_df = pd.DataFrame(columns=['ticker','g1','g2','g3'])
    for ticker in name_list:
        try:
            # get the df
            quarter_df = pd.read_sql('{}'.format(ticker),con=quarter_engine)
            # get the target time
            targettime = quarter_df.iloc[targetdate].datetime
            # use the mehtod get_selected_df
            selected_df = get_selected_df(selected_df, quarter_df, ticker, targetdate)
        except:
            print('{} not exsit'.format(ticker))
    # 删除inf
    selected_df = clean_df(selected_df)
    selected_df.to_csv('./results/selected_ticker_by_eps_{}.csv'.format(targettime),index=None)
    # selected_df.to_csv('selected_ticker_by_eps.csv',index=None)


# when target date equals to 0, means getting the lastest 
# when target date equals to 1, means getting the last quarter
def select_by_eps(targetdate = 0):
    # ignore the warnings
    pd.set_option('mode.chained_assignment', None)
    # get the name list 
    target_add = 'sqlite:///./././dataset/us/us_ticker_eps_quarter.db'
    name_list = get_name_list(target_add)
    print('name list got')
    # create the engine
    quarter_engine = create_engine(target_add)
    # create the select dataframe
    selected_df = pd.DataFrame(columns=['ticker','g1','g2','g3'])
    for ticker in name_list:
        try:
            # get the df
            quarter_df = pd.read_sql('{}'.format(ticker),con=quarter_engine)
            # get the target time
            targettime = quarter_df.iloc[targetdate].datetime
            # change to the method
            if len(quarter_df) < targetdate + 7:
                print('{} data not enough'.format(ticker))
                continue 
            quarter_df['growth_rate'] = 0
            for i in range(len(quarter_df)-4):
                quarter_df.growth_rate.iloc[i] = (quarter_df.eps.iloc[i] - quarter_df.eps.iloc[i+4]) / quarter_df.eps.iloc[i+4]
            # fix the growth rate
            quarter_df['fixed_growth_rate'] = 0
            for i in range(len(quarter_df)-1):
                quarter_df.fixed_growth_rate.iloc[i] = (quarter_df.growth_rate.iloc[i] + quarter_df.growth_rate.iloc[i+1]) / 2 
            # pick the ticker
            if quarter_df.iloc[targetdate].growth_rate > quarter_df.iloc[targetdate+1].growth_rate > quarter_df.iloc[targetdate+2].growth_rate > 0.2 or quarter_df.iloc[targetdate].growth_rate > 1:
                g1 = quarter_df.iloc[targetdate].growth_rate
                g2 = quarter_df.iloc[targetdate+1].growth_rate
                g3 = quarter_df.iloc[targetdate+2].growth_rate
                temp = pd.DataFrame([[ticker,g1,g2,g3]],columns=['ticker','g1','g2','g3'])
                selected_df = pd.concat([selected_df,temp])
                print('{} selected'.format(ticker))
            elif quarter_df.iloc[targetdate].fixed_growth_rate > quarter_df.iloc[targetdate+1].fixed_growth_rate > quarter_df.iloc[targetdate+2].fixed_growth_rate > 0.2 or quarter_df.iloc[targetdate].fixed_growth_rate > 1:
                g1 = quarter_df.iloc[targetdate].fixed_growth_rate
                g2 = quarter_df.iloc[targetdate+1].fixed_growth_rate
                g3 = quarter_df.iloc[targetdate+2].fixed_growth_rate
                temp = pd.DataFrame([[ticker,g1,g2,g3]],columns=['ticker','g1','g2','g3'])
                selected_df = pd.concat([selected_df,temp])
                print('{} selected'.format(ticker))
            else:
                print('{} not selected'.format(ticker))
        except:
            print('{} not exsit'.format(ticker))
    # 删除inf
    selected_df.replace([np.inf, -np.inf], np.nan,inplace=True)
    selected_df.dropna(axis=0, inplace=True)
    selected_df.index = range(len(selected_df))
    selected_df.to_csv('./results/selected_ticker_by_{}.csv'.format(targettime),index=None)
    # selected_df.to_csv('selected_ticker_by_eps.csv',index=None)

# engine = create_engine('sqlite:///./././dataset/us/us_ticker_revenue_mac.db')
def select_by_revenue(targetdate = 0):
    # ignore the warnings
    pd.set_option('mode.chained_assignment', None)
    # get the name list 
    target_add = 'sqlite:///./././dataset/us/us_ticker_revenue_mac.db'
    name_list = get_name_list(target_add)
    # create the engine
    engine = create_engine(target_add)
    selected_df = pd.DataFrame(columns=['ticker','g1','g2','g3'])
    for ticker in name_list:
        try:
            quarter_revenue = pd.read_sql('{}-Quarter'.format(ticker),con=engine)
            if len(quarter_revenue) < targetdate + 7:
                print('{} data not enough'.format(ticker))
                continue
            targettime = quarter_revenue.iloc[targetdate].datetime
            quarter_revenue['growth'] = 0
            for i in range(len(quarter_revenue)-4):
                quarter_revenue.growth.iloc[i] = (quarter_revenue.revenue.iloc[i] - quarter_revenue.revenue.iloc[i+4]) / quarter_revenue.revenue.iloc[i+4]
            # fix the growth rate
            quarter_revenue['fixed_growth'] = 0
            for i in range(len(quarter_revenue)-1):
                    quarter_revenue.fixed_growth.iloc[i] = (quarter_revenue.growth.iloc[i] + quarter_revenue.growth.iloc[i+1]) / 2 
            # pick the ticker
            if quarter_revenue.iloc[targetdate].growth > quarter_revenue.iloc[targetdate+1].growth > quarter_revenue.iloc[targetdate+2].growth > 0.2 or quarter_revenue.iloc[targetdate].growth > 1:
                g1 = quarter_revenue.iloc[targetdate].growth
                g2 = quarter_revenue.iloc[targetdate+1].growth
                g3 = quarter_revenue.iloc[targetdate+2].growth
                temp = pd.DataFrame([[ticker,g1,g2,g3]],columns=['ticker','g1','g2','g3'])
                selected_df = pd.concat([selected_df,temp])
                print('{} selected'.format(ticker))
            elif quarter_revenue.iloc[targetdate].fixed_growth > quarter_revenue.iloc[targetdate+1].fixed_growth > quarter_revenue.iloc[targetdate+2].fixed_growth > 0.2 or quarter_revenue.iloc[targetdate].fixed_growth > 1:
                g1 = quarter_revenue.iloc[targetdate].fixed_growth
                g2 = quarter_revenue.iloc[targetdate+1].fixed_growth
                g3 = quarter_revenue.iloc[targetdate+2].fixed_growth
                temp = pd.DataFrame([[ticker,g1,g2,g3]],columns=['ticker','g1','g2','g3'])
                selected_df = pd.concat([selected_df,temp])
                print('{} selected'.format(ticker))
            else:
                # print(g1,g2,g3)
                print('{} not selected'.format(ticker))
        except:
            print('{} not exsit'.format(ticker))
    # 删除inf
    selected_df.replace([np.inf, -np.inf], np.nan,inplace=True)
    selected_df.dropna(axis=0, inplace=True)
    selected_df.index = range(len(selected_df))
    selected_df.to_csv('./results/selected_ticker_by_{}.csv'.format(targettime),index=None)          
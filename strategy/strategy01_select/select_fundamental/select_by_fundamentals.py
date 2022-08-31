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

# when target date equals to 0, means getting the lastest 
# when target date equals to 1, means getting the last quarter
def select_by_eps(targetdate = 0):
    # ignore the warnings
    pd.set_option('mode.chained_assignment', None)
    # get the name list 
    target_add = 'sqlite:///./././dataset/us/us_ticker_eps_quarter.db'
    name_list = get_name_list(target_add)
    # create the engine
    quarter_engine = create_engine(target_add)
    # create the select dataframe
    selected_df = pd.DataFrame(columns=['ticker','eps_g1','eps_g2','eps_g3'])
    for ticker in name_list:
        try:
            quarter_eps = pd.read_sql('{}'.format(ticker),con=quarter_engine)
            if len(quarter_eps) < targetdate + 7:
                print('{} data not enough'.format(ticker))
                continue
            targettime = quarter_eps.iloc[targetdate].datetime
            quarter_eps['yoy_growth'] = 0
            for i in range(len(quarter_eps)-4):
                quarter_eps.yoy_growth.iloc[i] = (quarter_eps.eps.iloc[i] - quarter_eps.eps.iloc[i+4]) / quarter_eps.eps.iloc[i+4]
            # fix the growth rate
            quarter_eps['fixed_yoy_growth'] = 0
            for i in range(len(quarter_eps)-1):
                quarter_eps.fixed_yoy_growth.iloc[i] = (quarter_eps.yoy_growth.iloc[i] + quarter_eps.yoy_growth.iloc[i+1]) / 2 
            # pick the ticker
            if quarter_eps.iloc[targetdate].yoy_growth > quarter_eps.iloc[targetdate+1].yoy_growth > quarter_eps.iloc[targetdate+2].yoy_growth > 0.2 or quarter_eps.iloc[targetdate].yoy_growth > 1:
                eps_g1 = quarter_eps.iloc[targetdate].yoy_growth
                eps_g2 = quarter_eps.iloc[targetdate+1].yoy_growth
                eps_g3 = quarter_eps.iloc[targetdate+2].yoy_growth
                temp = pd.DataFrame([[ticker,eps_g1,eps_g2,eps_g3]],columns=['ticker','eps_g1','eps_g2','eps_g3'])
                selected_df = pd.concat([selected_df,temp])
                print('{} selected'.format(ticker))
            elif quarter_eps.iloc[targetdate].fixed_yoy_growth > quarter_eps.iloc[targetdate+1].fixed_yoy_growth > quarter_eps.iloc[targetdate+2].fixed_yoy_growth > 0.2 or quarter_eps.iloc[targetdate].fixed_yoy_growth > 1:
                eps_g1 = quarter_eps.iloc[targetdate].fixed_yoy_growth
                eps_g2 = quarter_eps.iloc[targetdate+1].fixed_yoy_growth
                eps_g3 = quarter_eps.iloc[targetdate+2].fixed_yoy_growth
                temp = pd.DataFrame([[ticker,eps_g1,eps_g2,eps_g3]],columns=['ticker','eps_g1','eps_g2','eps_g3'])
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
    selected_df.to_csv('./results/selected_ticker_by_eps_{}.csv'.format(targettime),index=None)
    # selected_df.to_csv('selected_ticker_by_eps.csv',index=None)

# revenue_engine = create_engine('sqlite:///./././dataset/us/us_ticker_revenue_mac.db')
def select_by_revenue(targetdate = 0):
    # ignore the warnings
    pd.set_option('mode.chained_assignment', None)
    # get the name list 
    target_add = 'sqlite:///./././dataset/us/us_ticker_revenue_mac.db'
    name_list = get_name_list(target_add)
    # create the engine
    revenue_engine = create_engine(target_add)
    selected_df = pd.DataFrame(columns=['ticker','revenue_g1','revenue_g2','revenue_g3'])
    for ticker in name_list:
        try:
            quarter_revenue = pd.read_sql('{}-Quarter'.format(ticker),con=revenue_engine)
            if len(quarter_revenue) < targetdate + 7:
                print('{} data not enough'.format(ticker))
                continue
            targettime = quarter_revenue.iloc[targetdate].datetime
            quarter_revenue['revenue_growth'] = 0
            for i in range(len(quarter_revenue)-4):
                quarter_revenue.revenue_growth.iloc[i] = (quarter_revenue.revenue.iloc[i] - quarter_revenue.revenue.iloc[i+4]) / quarter_revenue.revenue.iloc[i+4]
            # fix the growth rate
            quarter_revenue['fixed_revenue_growth'] = 0
            for i in range(len(quarter_revenue)-1):
                    quarter_revenue.fixed_revenue_growth.iloc[i] = (quarter_revenue.revenue_growth.iloc[i] + quarter_revenue.revenue_growth.iloc[i+1]) / 2 
            # pick the ticker
            if quarter_revenue.iloc[targetdate].revenue_growth > quarter_revenue.iloc[targetdate+1].revenue_growth > quarter_revenue.iloc[targetdate+2].revenue_growth > 0.2 or quarter_revenue.iloc[targetdate].revenue_growth > 1:
                revenue_g1 = quarter_revenue.iloc[targetdate].revenue_growth
                revenue_g2 = quarter_revenue.iloc[targetdate+1].revenue_growth
                revenue_g3 = quarter_revenue.iloc[targetdate+2].revenue_growth
                temp = pd.DataFrame([[ticker,revenue_g1,revenue_g2,revenue_g3]],columns=['ticker','revenue_g1','revenue_g2','revenue_g3'])
                selected_df = pd.concat([selected_df,temp])
                print('{} selected'.format(ticker))
            elif quarter_revenue.iloc[targetdate].fixed_revenue_growth > quarter_revenue.iloc[targetdate+1].fixed_revenue_growth > quarter_revenue.iloc[targetdate+2].fixed_revenue_growth > 0.2 or quarter_revenue.iloc[targetdate].fixed_revenue_growth > 1:
                revenue_g1 = quarter_revenue.iloc[targetdate].fixed_revenue_growth
                revenue_g2 = quarter_revenue.iloc[targetdate+1].fixed_revenue_growth
                revenue_g3 = quarter_revenue.iloc[targetdate+2].fixed_revenue_growth
                temp = pd.DataFrame([[ticker,revenue_g1,revenue_g2,revenue_g3]],columns=['ticker','revenue_g1','revenue_g2','revenue_g3'])
                selected_df = pd.concat([selected_df,temp])
                print('{} selected'.format(ticker))
            else:
                # print(revenue_g1,revenue_g2,revenue_g3)
                print('{} not selected'.format(ticker))
        except:
            print('{} not exsit'.format(ticker))
    # 删除inf
    selected_df.replace([np.inf, -np.inf], np.nan,inplace=True)
    selected_df.dropna(axis=0, inplace=True)
    selected_df.index = range(len(selected_df))
    selected_df.to_csv('./results/selected_ticker_by_revenue_{}.csv'.format(targettime),index=None)          
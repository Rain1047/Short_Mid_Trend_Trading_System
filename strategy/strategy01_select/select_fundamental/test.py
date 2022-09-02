# from select_by_fundamentals import select_by_eps_fixed as eps_fix
# from select_by_fundamentals import select_by_eps as eps

# eps()
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
            print('{} get'.format(ticker))
        except:
            name_list.remove(ticker)
    return name_list


def select_by_eps_fixed(targetdate = 0):
    # ignore the warnings
    pd.set_option('mode.chained_assignment', None)
    # get the name list 
    target_add = 'sqlite:///./././dataset/us/us_ticker_eps_quarter.db'
    name_list = get_name_list(target_add)
    print('name list got')
    return name_list
    

name_list = select_by_eps_fixed(0)
print(name_list)

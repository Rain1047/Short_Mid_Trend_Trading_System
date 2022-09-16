import pandas as pd
from pattern_cup import judge_cup as jc
from pattern_vcp import judge_vcp as jv
from pattern_db import judge_db as jd
# import tushare as ts 

def find_pattern(ticker_name, target_date):
    res = pd.DataFrame([['name','date',0,0,0]],columns=['ticker','datetime','vcp','cup','db'])
    res['ticker'] = ticker_name
    res['datetime'] = target_date
    if jv(ticker_name, target_date) == 100:
        # print('{} is vcp in {}'.format(ticker_name,target_date))
        res['vcp'] = 1
        return res
    elif jc(ticker_name, target_date) == 201:
        # print('{} is vcp in {}'.format(ticker_name,target_date))
        res['cup'] = 1
        return res
    elif jd(ticker_name, target_date) == 300:
        # print('{} might be double bottom in {}.'.format(ticker_name, target_date))
        res['db'] = 1
        return res
    else:
        print('{} not pattern in {}'.format(ticker_name, target_date))
        return res
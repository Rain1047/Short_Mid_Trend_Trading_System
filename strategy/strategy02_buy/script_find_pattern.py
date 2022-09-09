from pattern_cup import judge_cup as jc
from pattern_vcp import judge_vcp as jv
from pattern_db import judge_db as jd
import tushare as ts 

def find_pattern(ticker_name, target_date):
    if jv(ticker_name, target_date) == True:
        print('{} is vcp in {}'.format(ticker_name,target_date))
        return
    elif jc(ticker_name, target_date) == True:
        # print('{} is vcp in {}'.format(ticker_name,target_date))
        return
    elif jd(ticker_name, target_date) == True:
        print('{} might be double bottom in {}.'.format(ticker_name, target_date))
        return
    else:
        print('not pattern in {}'.format(target_date))
        return
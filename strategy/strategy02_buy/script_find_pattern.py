from pattern_cup import judge_cup as jc
from pattern_vcp import judge_vcp as jv
from pattern_db import judge_db as jb

def find_pattern(ticker_name, target_date):
    if jv(ticker_name, target_date) == True:
        return
    elif jc(ticker_name, target_date) == True:
        return
    elif jb(ticker_name, target_date) == True:
        return
    else:
        print('not pattern')
        return
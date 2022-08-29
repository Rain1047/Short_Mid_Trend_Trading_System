import baostock as bs
import pandas as pd

def get_sz50():
    # 登陆系统
    lg = bs.login()

    # 获取上证50成分股
    rs = bs.query_sz50_stocks()
    # 打印结果集
    sz50_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        sz50_stocks.append(rs.get_row_data())
    result = pd.DataFrame(sz50_stocks, columns=rs.fields)
    return result
    # 登出系统
    bs.logout()

def get_hs300():
# 登陆系统
    lg = bs.login()
    # 获取沪深300成分股
    rs = bs.query_hs300_stocks()
    # 打印结果集
    hs300_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        hs300_stocks.append(rs.get_row_data())
    result = pd.DataFrame(hs300_stocks, columns=rs.fields)
    # 结果集输出到csv文件
    return result
    # 登出系统
    bs.logout()

def get_zz500():
    # 登陆系统
    lg = bs.login()

    # 获取中证500成分股
    rs = bs.query_zz500_stocks()

    # 打印结果集
    zz500_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        zz500_stocks.append(rs.get_row_data())
    result = pd.DataFrame(zz500_stocks, columns=rs.fields)
    return result
    # 登出系统
    bs.logout()

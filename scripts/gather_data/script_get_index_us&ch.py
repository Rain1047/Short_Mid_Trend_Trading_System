# import libraries
import urllib.request
from urllib.request import urlopen
import urllib.parse
import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
import baostock as bs

# -----------------------------------#
# China:
# 上证50 get_sz50()
# 沪深300 get_hs300()
# 中证500 get_zz500()
# US:
# Nasdaq100 get_nasdaq100()
# SP500 get_sp500()
# -----------------------------------#

# China
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

# US
# define the header
# write your own header here
# get your header at "chrome://version"
headers = {'User-Agent':'Mozilla/5.0 Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62'}
# nasdaq100
def get_nasdaq100():
    # define the url
    html_data = requests.get('https://www.slickcharts.com/nasdaq100',headers=headers)
    # make the soup
    soup = BeautifulSoup(html_data.text, 'lxml')
    # find the right table
    target_table = soup.find_all('table', attrs={'class':'table'})[0]

    # create the dataframe
    nasdaq100 = pd.DataFrame(columns=['symbol','company','weight'])
    for row in target_table.find_all('tr'):
        col = row.find_all('td')
        if len(col) == 7:
            symbol = col[2].text
            weight = col[3].text
            company = col[1].text
            temp = pd.DataFrame([[symbol,company,weight]],columns=['symbol','company','weight'])
            nasdaq100 = pd.concat([nasdaq100, temp],ignore_index=True)
    return nasdaq100

# sp500
def get_sp500():
    # define the url
    html_data = requests.get('https://www.slickcharts.com/sp500',headers=headers)
    # make the soup
    soup = BeautifulSoup(html_data.text, 'lxml')
    # find the right table
    target_table = soup.find_all('table', attrs={'class':'table'})[0]

    # create the dataframe
    sp500 = pd.DataFrame(columns=['symbol','company','weight'])
    for row in target_table.find_all('tr'):
        col = row.find_all('td')
        if len(col) == 7:
            symbol = col[2].text
            weight = col[3].text
            company = col[1].text
            temp = pd.DataFrame([[symbol,company,weight]],columns=['symbol','company','weight'])
            sp500 = pd.concat([sp500, temp],ignore_index=True)
    return sp500

# dowjones
def get_dowjones50():
    # define the url
    html_data = requests.get('https://www.slickcharts.com/dowjones',headers=headers)
    # make the soup
    soup = BeautifulSoup(html_data.text, 'lxml')
    # find the right table
    target_table = soup.find_all('table', attrs={'class':'table'})[0]

    # create the dataframe
    dowjones50 = pd.DataFrame(columns=["symbol", "weight"])

    for row in target_table.find_all('tr'):
        col = row.find_all('td')
        if len(col) == 7:
            symbol = col[2].text
            weight = col[3].text
            dowjones50 = dowjones50.append({'symbol':symbol, 'weight':weight},ignore_index=True)
    return dowjones50
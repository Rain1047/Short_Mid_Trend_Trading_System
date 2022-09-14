# import libraries
import urllib.request
from urllib.request import urlopen
import urllib.parse
import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

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
    nasdaq_100 = pd.DataFrame(columns=["symbol", "weight"])

    for row in target_table.find_all('tr'):
        col = row.find_all('td')
        if len(col) == 7:
            symbol = col[2].text
            weight = col[3].text
            nasdaq_100 = nasdaq_100.append({'symbol':symbol, 'weight':weight},ignore_index=True)
    return nasdaq_100

# sp500
def get_sp500():
    # define the url
    html_data = requests.get('https://www.slickcharts.com/sp500',headers=headers)
    # make the soup
    soup = BeautifulSoup(html_data.text, 'lxml')
    # find the right table
    target_table = soup.find_all('table', attrs={'class':'table'})[0]

    # create the dataframe
    sp500 = pd.DataFrame(columns=["symbol", "weight"])

    for row in target_table.find_all('tr'):
        col = row.find_all('td')
        if len(col) == 7:
            symbol = col[2].text
            weight = col[3].text
            sp500 = sp500.append({'symbol':symbol, 'weight':weight},ignore_index=True)
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
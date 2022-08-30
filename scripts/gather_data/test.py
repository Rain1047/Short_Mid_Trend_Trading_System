import pandas as pd
import requests
import urllib.parse
import urllib.request
import sqlite3
from urllib.request import urlopen
from sqlalchemy import create_engine
from datetime import datetime as dt
from bs4 import BeautifulSoup

def print_a(a=0):
    print(a)

print_a()
print_a(2)

def get_name_list(start=0):
        # create database connection
        ticker_engine = create_engine('sqlite:///././dataset/us/us_ticker_list_with_name.db')
        ticker_df = pd.read_sql('TOTAL',ticker_engine)
        ticker_df = ticker_df[start:]
        # convert to list
        ticker_symbol_list = ticker_df.Symbol.to_list()
        ticker_name_list = ticker_df['Company Name'].to_list()
        return ticker_symbol_list, ticker_name_list

def use_get_list(start=0):
    ticker_symbol_list,ticker_name_list = get_name_list(start)
    print(ticker_name_list[:20])
    print(ticker_symbol_list[:20])

use_get_list(10)
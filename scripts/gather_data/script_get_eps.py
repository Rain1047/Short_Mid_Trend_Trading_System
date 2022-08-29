import pandas as pd
import requests
import urllib.parse
import urllib.request
import sqlite3
from urllib.request import urlopen
from sqlalchemy import create_engine
from datetime import datetime as dt
from bs4 import BeautifulSoup

# define the header
# write your own header here
# get your header at "chrome://version"
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}


rt = dt.now()
runtime = str(rt.year) + str(rt.month) + str(rt.day)
# # define a processing bar
from tqdm import tqdm
# import sys, time
# def process_bar(num, total):
#         rate = float(num)/total
#         ratenum =  int(100*rate)
#         r = '\r[{}{}]{}%'.format('*'*ratenum,' '*(100-ratenum), ratenum)
#         sys.stdout.write(r)
#         sys.stdout.flush()

def get_eps(start):
        # create database connection
        ticker_engine = create_engine('sqlite:///././dataset/us/us_ticker_list_with_name.db')
        ticker_df = pd.read_sql('TOTAL',ticker_engine)
        # ticker_list = pd.read_csv('ticker_list_with_name.csv')
        ticker_df = ticker_df[start:]
        # convert to list
        ticker_symbol_list = ticker_df.Symbol.to_list()
        ticker_name_list = ticker_df['Company Name'].to_list()
        ticker_length = len(ticker_symbol_list)
        # create engine
        annual_engine = create_engine('sqlite:///././dataset/us/us_ticker_eps_annual.db')
        quarter_engine = create_engine('sqlite:///././dataset/us/us_ticker_eps_quarter.db')

        # record result
        log_df = pd.DataFrame(columns=['symbol','status'])
        log_engine = create_engine('sqlite:///././dataset/us/us_log_record.db')
        for i in tqdm(range(ticker_length)):
                try:
                        html_data = requests.get('https://www.macrotrends.net/stocks/charts/{}/{}/eps-earnings-per-share-diluted'.format(ticker_symbol_list[i], ticker_name_list[i]),headers=headers, timeout=10)
                        soup = BeautifulSoup(html_data.text, 'lxml')
                        target_table = soup.find_all('table', attrs={'class':'historical_data_table'})
                        # # Annual
                        target_table_01 = target_table[0]
                        ticker_eps_annual = pd.DataFrame(columns=['datetime','eps'])
                        # ------------------------------- # 
                        #        get annual eps
                        # ------------------------------- #
                        for row in target_table_01.find_all('tr'):
                                col = row.find_all('td')
                                len_col = len(col)
                                if len_col == 2:
                                        date = col[0].text
                                        eps = col[1].text[1:]
                                        temp = pd.DataFrame([[date, eps]],columns=['datetime','eps'])
                                        ticker_eps_annual = pd.concat([ticker_eps_annual,temp],ignore_index=True)
                        ticker_eps_annual.eps = ticker_eps_annual.eps.astype(float)
                        ticker_eps_annual.to_sql('{}'.format(ticker_symbol_list[i]), con=annual_engine, if_exists='replace',index=None)
                        
                        # ------------------------------- # 
                        #        get annual eps
                        # ------------------------------- #
                        # Quarter 
                        target_table_02 = target_table[1]
                        ticker_eps_quarter = pd.DataFrame(columns=['datetime','eps'])
                        for row in target_table_02.find_all('tr'):
                                col = row.find_all('td')
                                len_col = len(col)
                                if len_col == 2:
                                        date = col[0].text
                                        eps = col[1].text[1:]
                                        temp = pd.DataFrame([[date, eps]],columns=['datetime','eps'])
                                        ticker_eps_quarter = pd.concat([ticker_eps_quarter,temp],ignore_index=True)
                        ticker_eps_quarter.eps = ticker_eps_quarter.eps.astype(float)
                        ticker_eps_quarter.to_sql('{}'.format(ticker_symbol_list[i]),con=quarter_engine, if_exists='replace',index=None)
                        print('No.{} {} ok'.format(i,ticker_symbol_list[i]))
                        # status = 'ok'
                        # temp_log = pd.DataFrame([[ticker_symbol_list[i], status]], columns=['symbol', 'status'])
                        # log_df = pd.concat([log_df,temp_log])
                except:
                        status = 'fail'
                        temp_log = pd.DataFrame([[ticker_symbol_list[i], status]], columns=['symbol', 'status'])
                        log_df = pd.concat([log_df,temp_log])
                        log_df.to_sql('{} eps record'.format(runtime),con=log_engine,if_exists='replace',index=None)


def get_roe(start):
        # create database connection
        ticker_engine = create_engine('sqlite:///././dataset/us/us_ticker_list_with_name.db')
        ticker_df = pd.read_sql('TOTAL',ticker_engine)
        ticker_df = ticker_df[start:]
        # convert to list
        ticker_symbol_list = ticker_df.Symbol.to_list()
        ticker_name_list = ticker_df['Company Name'].to_list()
        ticker_length = len(ticker_symbol_list)
        # create engine
        roe_engine = create_engine('sqlite:///././dataset/us/us_ticker_roe.db')
        # record result
        log_df = pd.DataFrame(columns=['symbol','status'])
        log_engine = create_engine('sqlite:///././dataset/us/us_log_record.db')
        for i in tqdm(range(ticker_length)):
                try:
                        html_data = requests.get('https://www.macrotrends.net/stocks/charts/{}/{}/roe'.format(ticker_symbol_list[i], ticker_name_list[i]),headers=headers, timeout=10)
                        soup = BeautifulSoup(html_data.text, 'lxml')
                        target_table = soup.find_all('table')
                        target_table_01 = target_table[0]
                        ticker_roe = pd.DataFrame(columns=['datetime','ttm',"shareholder'sEquity",'roe'])
                        # ------------------------------- # 
                        #           get roe
                        # ------------------------------- #
                        for row in target_table_01.find_all('tr'):
                                col = row.find_all('td')
                                len_col = len(col)
                                if len_col == 4:
                                        date = col[0].text
                                        ttm = col[1].text[1:-1]
                                        se = col[2].text[1:-1]
                                        roe = col[3].text[:-1]
                                        temp = pd.DataFrame([[date, ttm, se, roe]],columns=['datetime','ttm',"shareholder'sEquity",'roe'])
                                        ticker_roe = pd.concat([ticker_roe,temp],ignore_index=True)
                        ticker_roe.roe = ticker_roe.roe.astype(float)
                        ticker_roe.to_sql('{}'.format(ticker_symbol_list[i]), con=roe_engine, if_exists='replace',index=None)
                except:
                        status = 'fail'
                        temp_log = pd.DataFrame([[ticker_symbol_list[i], status]], columns=['symbol', 'status'])
                        log_df = pd.concat([log_df,temp_log])
                        log_df.to_sql('{} roe record'.format(runtime),con=log_engine,if_exists='replace',index=None)         

def get_pe(start):
        # create database connection
        ticker_engine = create_engine('sqlite:///././dataset/us/us_ticker_list_with_name.db')
        ticker_df = pd.read_sql('TOTAL',ticker_engine)
        ticker_df = ticker_df[start:]
        # convert to list
        ticker_symbol_list = ticker_df.Symbol.to_list()
        ticker_name_list = ticker_df['Company Name'].to_list()
        ticker_length = len(ticker_symbol_list)
        # create engine
        pe_engine = create_engine('sqlite:///././dataset/us/us_ticker_pe.db')
        # record result
        log_df = pd.DataFrame(columns=['symbol','status'])
        log_engine = create_engine('sqlite:///././dataset/us/us_log_record.db')
        for i in tqdm(range(ticker_length)):
                try:
                        html_data = requests.get('https://www.macrotrends.net/stocks/charts/{}/{}/pe-ratio'.format(ticker_symbol_list[i], ticker_name_list[i]),headers=headers, timeout=10)
                        soup = BeautifulSoup(html_data.text, 'lxml')
                        target_table = soup.find_all('table')
                        target_table_01 = target_table[0]
                        ticker_pe = pd.DataFrame(columns=['datetime','pe_ratio'])
                        # ------------------------------- # 
                        #           get pe-ratio
                        # ------------------------------- #
                        for row in target_table_01.find_all('tr'):
                                col = row.find_all('td')
                                len_col = len(col)
                                if len_col == 4:
                                        date = col[0].text
                                        pe = col[3].text
                                        temp = pd.DataFrame([[date, pe]],columns=['datetime','pe_ratio'])
                                        ticker_pe = pd.concat([ticker_pe,temp],ignore_index=True)
                        ticker_pe.pe_ratio = ticker_pe.pe_ratio.astype(float)
                        ticker_pe.to_sql('{}'.format(ticker_symbol_list[i]), con=pe_engine, if_exists='replace',index=None)
                except:
                        status = 'fail'
                        temp_log = pd.DataFrame([[ticker_symbol_list[i], status]], columns=['symbol', 'status'])
                        log_df = pd.concat([log_df,temp_log])
                        log_df.to_sql('{} pe/ratio record'.format(runtime),con=log_engine,if_exists='replace',index=None)         

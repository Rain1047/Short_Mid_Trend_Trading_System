# Pandas
import pandas as pd
import talib as ta
import numpy as np
from get_score import get_score_ch
from get_pyechart import plot_kchart
from sqlalchemy import create_engine
from get_pyechart import plot_kchart


def getdf(ticker):
    engine= create_engine('sqlite:///../../single_ticker_price/ch/ch_ticker_price.db')
    df = pd.read_sql('{}'.format(ticker), engine)
    return df
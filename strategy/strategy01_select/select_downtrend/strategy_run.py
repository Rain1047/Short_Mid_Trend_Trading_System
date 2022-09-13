import pandas as pd
from sqlalchemy import create_engine

# get ticker list 
ticker_df = pd.read_sql('TOTAL', con=ticker_engine)
ticker_list = ticker_df.Symbol.to_list()


import pandas as pd
from sqlalchemy import create_engine
import tushare as ts
from strategy_downtrend import downtrend_strategy as ds



df = pd.DataFrame([[1,2,3,4]])
df.to_sql('test', con=downtrend_engine)

price_path = r"dataset\us\us_ticker_seven_year_price.db"
import pandas as pd
from sqlalchemy import create_engine

price_engine = create_engine('sqlite:///{}'.format(price_path))
df = pd.read_sql('AAPL',con=price_engine)
print(df)
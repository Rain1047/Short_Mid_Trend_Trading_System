import pandas as pd
from sqlalchemy import create_engine
res_engine = create_engine('sqlite:///strategy\strategy01_select\select_technical\select_test_result\select_test_result.db')

df = pd.DataFrame([[1,2,43,45,123,2,523,523]])
df.to_sql('test',con=res_engine,if_exists='replace')

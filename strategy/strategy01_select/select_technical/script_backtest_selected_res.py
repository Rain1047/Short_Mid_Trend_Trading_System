import pandas as pd
from sqlalchemy import create_engine

def backtest_res(target_date):
    # create engine
    price_engine = create_engine('sqlite:///./././dataset/us/us_ticker_seven_year_price.db')
    result_engine = create_engine('sqlite:///strategy\strategy01_select\select_technical\select_result\select_result.db')
    b_result_engine = create_engine('sqlite:///strategy\strategy01_select\select_technical\select_test_result\select_test_result.db')
    # create the test result
    res = pd.read_sql('{}_res'.format(target_date),con=result_engine)
    test_result = pd.DataFrame(columns=['profit_avg_60','profit_avg_90','profit_avg_120','decline_avg_60','declince_avg_90','decline_avg_120'])
    test_count = 10000
    for i in range(test_count):
        # 抽样
        samples = res.sample(10,replace=True)
        samples_list = samples.ticker.to_list()
        # store the data 
        profit_avg_60 = 0.0
        profit_avg_90 = 0.0
        profit_avg_120 = 0.0
        decline_avg_60 = 0.0
        decline_avg_90 = 0.0
        decline_avg_120 = 0.0
        for sample in samples_list:
            try:
                # print(sample)
                sample_price_df = pd.read_sql('{}'.format(sample), con=price_engine)
                start_index = sample_price_df[sample_price_df.datetime == target_date].index.values[0]
                start_price = sample_price_df[sample_price_df.datetime == target_date].Close.values[0]
                if start_price < 12:
                    break
                else:
                    sample_price_df = sample_price_df[start_index:]
                    sample_price_df.index = range(len(sample_price_df))
                    # 
                    max_60 = sample_price_df[0:410].Close.max()
                    min_60 = sample_price_df[0:410].Close.min()
                    max_90 = sample_price_df[0:65].Close.max()
                    min_90 = sample_price_df[0:65].Close.min()
                    max_120 = sample_price_df[0:85].Close.max()
                    min_120 = sample_price_df[0:85].Close.min()
                    # print(start_price,max_60,max_90,max_120)
                    # 
                    profit_60 = (max_60 - start_price) / start_price
                    profit_90 = (max_90 - start_price) / start_price
                    profit_120 = (max_120 - start_price) / start_price
                    decline_60 = (min_60 - start_price) / start_price
                    decline_90 = (min_90 - start_price) / start_price
                    decline_120 = (min_120 - start_price) / start_price
                    # print(profit_60,profit_90,profit_120)
                    # 
                    profit_avg_60 += profit_60
                    profit_avg_90 += profit_90
                    profit_avg_120 += profit_120
                    decline_avg_60 += decline_60
                    decline_avg_90 += decline_90
                    decline_avg_120 += decline_120

            except:
                print('{} is wrong, result invalued'.format(sample))
                break
        profit_avg_60 = profit_avg_60 / 10
        profit_avg_90 = profit_avg_90 / 10
        profit_avg_120 = profit_avg_120 / 10
        decline_avg_60 = decline_avg_60 / 10
        decline_avg_90 = decline_avg_90 / 10
        decline_avg_120 = decline_avg_120 / 10
        temp = pd.DataFrame([[profit_avg_60,profit_avg_90,profit_avg_120,decline_avg_60,decline_avg_90,decline_avg_120]],columns=['profit_avg_60','profit_avg_90','profit_avg_120','decline_avg_60','declince_avg_90','decline_avg_120'])
        test_result = pd.concat([test_result, temp],ignore_index=True)
    # test_result.to_csv('backtest_result/{}_test_result.csv'.format(target_date),index=None)
    test_result.to_sql('{}_test_res_large'.format(target_date),if_exists='replace',index=None, con=b_result_engine)
    
        
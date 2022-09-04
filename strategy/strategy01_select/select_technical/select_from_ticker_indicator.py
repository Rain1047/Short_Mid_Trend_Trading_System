import pandas as pd 
from sqlalchemy import create_engine
ticker_engine = create_engine('sqlite:///./././dataset/us/us_ticker_with_indicator.db')
price_engine = create_engine('sqlite:///./././dataset/us/us_ticker_seven_year_price.db')

def select_from_ticker_indicator(target_date):
    # 得到res
    df = pd.read_sql('{}'.format(target_date), con=ticker_engine)
    df = df.query('Close > MA20 and Close > year_low*1.25 and Close > year_high * 0.75 and Close> 12 and MA20 > MA50 > MA200')
    df.index = range(len(df))
    df['rs_rank'] = 0
    for i in range(len(df)):
        val = df.iloc[i].rs
        df['rs_rank'].iloc[i] = int(round(df[df.rs < val].rs.count()  / len(df),2)*100)
    res = df.sort_values(by='rs_rank', ascending=False)
    # ticker_list = res[res.rs_rank > 75].symbol.to_list()
    res = res.query('rs_rank >= 70 and rs_rank <= 95')

    # create the test result
    test_result = pd.DataFrame(columns=['profit_avg_60','profit_avg_90','profit_avg_120','decline_avg_60','declince_avg_90','decline_avg_120'])
    test_count = 10000
    for i in range(test_count):
        # 抽样
        samples = res.sample(3)
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
                start_index = sample_price_df[sample_price_df.datetime == trade_date].index.values[0]
                start_price = sample_price_df[sample_price_df.datetime == trade_date].Close.values[0]
                if start_price < 12:
                    break
                else:
                    sample_price_df = sample_price_df[start_index:]
                    sample_price_df.index = range(len(sample_price_df))
                    # 
                    max_60 = sample_price_df[0:43].Close.max()
                    min_60 = sample_price_df[0:43].Close.min()
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
        profit_avg_60 = profit_avg_60 / 3
        profit_avg_90 = profit_avg_90 / 3
        profit_avg_120 = profit_avg_120 / 3
        decline_avg_60 = decline_avg_60 / 3
        decline_avg_90 = decline_avg_90 / 3
        decline_avg_120 = decline_avg_120 / 3
        temp = pd.DataFrame([[profit_avg_60,profit_avg_90,profit_avg_120,decline_avg_60,decline_avg_90,decline_avg_120]],columns=['profit_avg_60','profit_avg_90','profit_avg_120','decline_avg_60','declince_avg_90','decline_avg_120'])
        test_result = pd.concat([test_result, temp],ignore_index=True)
    test_result.to_csv('{}_test_result.csv'.format(target_date),index=None)
    
        
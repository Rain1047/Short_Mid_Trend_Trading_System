# from tkinter import N
import yfinance as yf

# ticker_list 

# ticker_name
for ticker in ticker_list:
    ticker = yf.Ticker("{}").format(ticker)

# ----------------------------------------#
# C=当季每股收益：对于一支股票来说，C值越高越好
# 当季每股净收益 earnings per share (quartlerly)
# 每股净收益 = （税后净收益 - 优先股股息）/ 发行在外普通股股数 
# 1季报：每年4月1日-4月30日
# 2季报（中报）：每年7月1日-8月30日
# 3季报：每年10月1日-10月31日
# 4季报（年报）：每年1月1日-4月30日
# ----------------------------------------#

# 季度税后净收益
earnings_quarterly = ticker.quarterly_earnings
# 当季发行在外的股票数 #! 需要调试
# https://www.sharesoutstandinghistory.com/?symbol=AAPL
nums_of_shares = ticker.info['sharesOutstanding']
# 计算每股收益(earnings per shares)
earnings_quarterly['eps'] = earnings_quarterly.Earnings / nums_of_shares
# 4季度平均每股收益
earnings_quarterly['eps'].mean()
# 当季每股收益和当年最高差值
currect_eps_diff = earnings_quarterly.tail(1)['eps'].values[0] - earnings_quarterly.eps.max()

# 计算每股收益增长率
# 短期每股收益增长率 STfwdEPS(#! target)
earnings_quarterly['STfwdEPS'] = (earnings_quarterly.eps.diff().fillna(0) / earnings_quarterly.eps.shift(1).fillna(1) * 100)
# 3季平均每股收益增长率
average_st_eps = earnings_quarterly[1:].STfwdEPS.mean()
#! 需要调整 
# 3季度每股收益增长率>0的个数
count_eps = earnings_quarterly[earnings_quarterly.STfwdEPS > 0].eps.count()
# 长期每股收益增长率 LTfwdEPS

# ----------------------------------------#
# A=每股收益年度增长率：找出每股收益真正增长的潜力股
# 年度每股收益增长率
# ----------------------------------------#

# 年度税后净收益
earnings_annually = ticker.earnings()
# 当年发行在外的股票数（以第四季度的数据为准）
nums_of_shares = ticker.info['shareOutstanding']
# 计算年度每股收益
earnings_annually['eps'] = earnings_annually.Earning / nums_of_shares
# 3年每股收益年度增长率
earnings_annually['STfwdEPS'] = (earnings_annually.eps.diff().fillna(0) / earnings_annually.eps.shift(1).fillna(1)*100)
# 3年平均每股收益年度增长率(#! target)
annual_average_st_eps = earnings_annually[1:].STfwdEPS.mean()
# 3年度每股收益>0的个数
annual_eps_count = earnings_annually[earnings_annually.STfwdEPS > 0].eps.count()


# ----------------------------------------#
# N=新产品、新管理阶层、股价新高：选择怎样的入市时机
#! 价格分析：
# 股价新高：用价格捕捉，在价格系统中进行筛选
# ----------------------------------------#

# ----------------------------------------#
# S=供给与需求：股票发行量和大额交易需求量
# 资产负债率
# 投资人可以注意那些 #! 过去两三年内负债比率持续下降公司的股票
# ----------------------------------------#
balance_sheet = ticker.balance_sheet.T[['Total Assets','Short Long Term Debt','Long Term Debt']]
balance_sheet = balance_sheet.astype(float)
balance_sheet['Total Debt'] = balance_sheet['Short Long Term Debt'] + balance_sheet['Long Term Debt']
balance_sheet['Debt Ratio'] = round(balance_sheet['Total Debt'] / balance_sheet['Total Assets'] , 4)
# 近四年、三年、两年是否递减
if balance_sheet['Debt Ratio'].is_monotonic_increasing == True:
    print('2,3,4')
elif balance_sheet[:3]['Debt Ratio'].is_monotonic_increasing == True:
    print('2,3')
elif balance_sheet[:2]['Debt Ratio'].is_monotonic_increasing == True:
    print('2')

# ----------------------------------------#
#! 价格分析：
# 供应和需求
# 股票的单日成交量是评估供需情况的最佳指标。如果一支股票的价格发生回落，
# 你就必须观察一下交易量是否萎缩。如果交易萎缩，则意味着市场有卖空的压力。
# 如果股票价格上升，你要进一步观察交易量是否有显著扩张，
# 这种情况下很可能是由于机构投资者在买进此种股票建仓的缘故。
#! 进一步查看
# 一旦股票自底部整理形态（见第12章 关于如何阅读股价图以及识别领导股的价格形态）向上突破之后，
# 日成交量应该较正常水准至少高出50%，有的时候甚至可能超过100%或者更高。
# ----------------------------------------#


# ----------------------------------------#
#! 价格分析
# RS评级是用于比较一支特定股票在过去一年（52周）
# 内相对于市场其他股票的价格表现的一种专利评级。
# 简而言之：大家都跌的时候我跌的少，大家都涨的时候我才能涨得快
# ----------------------------------------#


# ----------------------------------------#
# I=机构投资者的认同：跟随领导者
# 知名持有者等
# ----------------------------------------#


# ----------------------------------------#
# M=市场走向：如何判断大盘走势 Market
# SP500 & Nasdaq
# 要想识别大盘顶点，你就要紧密跟踪每天的标准普尔500、纳斯达克指数。
# 在上涨行情中，必有某一天市场成交总量较前一天会有增加，
# 但是其指数却会出现回落倾向（主要表现是这一天的价格涨幅明显小于前一天的价格涨幅）
# ----------------------------------------#
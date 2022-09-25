# Python实用宝典
# 2020/04/20
# 转载请注明出处
import datetime
import os.path
import sys
import backtrader as bt
from backtrader.indicators import EMA
# import the package after installation
from backtrader_plotly.plotter import BacktraderPlotly
from backtrader_plotly.scheme import PlotScheme
import plotly.io
from sqlalchemy import create_engine
import pandas as pd
class TestStrategy(bt.Strategy):
    # 设置全局参数
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    @staticmethod
    def percent(today, yesterday):
        return float(today - yesterday) / today

    # 初始化变量
    def __init__(self):
        # 获得指定的价格序列
        self.dataclose = self.datas[0].close
        self.volume = self.datas[0].volume
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 添加指标
        ## macd快线
        me1 = EMA(self.data, period=12)
        me2 = EMA(self.data, period=26)
        self.macd = me1 - me2
        self.signal = EMA(self.macd, period=9)

        bt.indicators.MACDHisto(self.data)

    # 记录购买时的价格
    def notify_order(self, order):
        # 如果有一单正在进行或者已经被接受，则返回。保证同一时间只有一个订单正在进行
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果目前的订单都已经完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                # 记录买入时候的价格
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.bar_executed_close = self.dataclose[0]
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    # Python 实用宝典
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return

        if not self.position:
            # 昨天的macd diff
            condition1 = self.macd[-1] - self.signal[-1]
            # 今天的macd diff
            condition2 = self.macd[0] - self.signal[0]
            # 如果昨天的macd<0 今天的macd>0，则买入
            if condition1 < 0 and condition2 > 0:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

        else:
            # 否则定义
            condition = (self.dataclose[0] - self.bar_executed_close) / self.dataclose[0]
            if condition > 0.1 or condition < -0.1:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    # 获得数据
    # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, 'aapl_price.csv')
    # 从数据库获取
    database_us = 'sqlite:///dataset/database_ch.db'
    engine = create_engine(database_us)
    df = pd.read_sql('600000.SH',con=engine)
    df.trade_date = pd.to_datetime(df.trade_date)
    df = df[::-1]
    print(df.dtypes)

    # 加载数据到模型中
    # data = bt.feeds.GenericCSVData(
    #     dataname=datapath,
    #     fromdate=datetime.datetime(2010, 1, 1),
    #     todate=datetime.datetsime(2020, 4, 12),
    #     dtformat='%Y%m%d',
    #     datetime=6,
    #     open=0,
    #     high=1,
    #     low=2,
    #     close=3,
    #     volume=5,
    #     reverse=True
    # )
    # data = 
    data = bt.feeds.PandasData(
        dataname=df,
        fromdate=datetime.datetime(2011, 1, 1),
        todate=datetime.datetime(2012, 12, 31),
        datetime='trade_date',
        open='open',
        high='high',
        low='low',    
        close='close',
        volume='vol',
        openinterest=-1
    )
    print(data)
    cerebro.adddata(data)

    cerebro.broker.setcash(10000)

    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    cerebro.broker.setcommission(commission=0.005)
    
    # 获取初识价格
    start_portfolio = cerebro.broker.getvalue()
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # 运行程序
    cerebro.run()
    # 获取最终价格
    final_portfolio = cerebro.broker.getvalue()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    portfolio_rate = round((final_portfolio - start_portfolio) / start_portfolio,2)
    print('Portfolio Rare:{}'.format(portfolio_rate))
    
    # cerebro.plot()
    # define plot scheme with new additional scheme arguments
    scheme = PlotScheme(decimal_places=5, max_legend_text_width=16)

    # plot and save figures as `plotly` graph object
    figs = cerebro.plot(BacktraderPlotly(show=True, scheme=scheme))
    figs = [x for fig in figs for x in fig]  # flatten output
    for fig in figs:
        plotly.io.to_html(fig, full_html=False)  # open html in the browser
        plotly.io.write_html(fig, file=r'strategy\strategy04_backtest\backtesting_trade\test_result\plot2.html')  # save the html file
        # plotly.offline.plot(fig, filename='file1.html')
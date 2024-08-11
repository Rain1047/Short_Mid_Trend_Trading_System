# 中长线交易系统/Medium to long term trading system

## 中文/Chinese

<center><font size=5>简介</font></center>

在本项目中，我们从收集最基本的数据开始，到输出筛选的股票和判断买入的时机结束。从0开始，构建了一个具有更新数据（基本面、技术面）、选股、判断买入、判断卖出完整的中长线趋势交易系统。

我的项目结构如下所示：

1. -dataset：存放主要的数据库
2. -document：项目设计思路、改进以及在这个过程中的收获和感悟
3. -scripts：主要的脚本，用于收集、整理数据，以及对数据的可视化处理
4. -strategy：项目核心，包含了系统的各个组成部分
5. -ticker_analysis：单个股票的分析
6. -trading_system：未来实现自动化交易的接口（未完成）

### 数据收集

|              | 美股                     | A股                 |
| ------------ | ------------------------ | ------------------- |
| 股票列表     | √ yfinance（前复权）     | √ baostock          |
| 基本面数据   | √ 爬虫方式 beautifulsoup | √ tushare           |
| 历史日线数据 | √ yfinance（前复权）     | √ tushare（前复权） |

### 选股系统

| 选股方案     | 详情                                                         |
| ------------ | ------------------------------------------------------------ |
| 基本面选股   | [基本面选股详情](https://github.com/Rain1047/Short_Mid_Trend_Trading_System/blob/main/document/strategy01a_select_fundamental.md) |
| 技术面选股   | [技术面选股详情](https://github.com/Rain1047/Short_Mid_Trend_Trading_System/blob/main/document/strategy01b_select_technical.md) |
| 下降趋势选股 | [大盘进入下降周期时选股](https://github.com/Rain1047/Short_Mid_Trend_Trading_System/blob/main/document/strategy01c_select_downtrend.md) |

### 买入卖出系统

（文档正在整理中）

主要分为两种思路：一为判断形态买入卖出，二为判断量价背离买入卖出

### 回测系统

使用backtest实现了简单策略的历史回测:

<a href="https://imgur.com/0d6w1em"><img src="https://i.imgur.com/0d6w1em.png" title="source: imgur.com" /></a>

## English/英文

<center><font size=5>brief introduction</font></center>

In this project, we start by collecting the most basic data, and end by outputting the stocks to be screened and judging the timing of buying. Starting from 0, and finally building a complete medium and long-term trend trading system with stock selection, judgment to buy, and judgment to sell has been constructed.

Our project structure looks like this:

1. -dataset: store the main database
2. -document: project design ideas, improvements, and gains and insights in the process
3. -scripts: The main scripts used to collect, organize, and visualize data
4. -strategy: the core of the project, which contains the various components of the system
5. -ticker_analysis: Analysis of a single stock
6. -trading_system: The interface for implementing automated trading in the future (unfinished)
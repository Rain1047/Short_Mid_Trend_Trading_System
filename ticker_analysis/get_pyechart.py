# pandas and numpy
import requests
import numpy as np 
import pandas as pd 
# import data
import sqlite3
# list seq and union
from typing import List, Sequence, Union
# TA-Lib
import talib as ta
# pyechart
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Kline, Line, Bar, Grid
from get_df import getdf

def plot_kchart(data):
    df = data
    df[['open','high', 'low', 'close','volume', 'amount', 'pctChg']] = df[['open','high', 'low', 'close', 'volume', 'amount', 'pctChg']].astype(float)
    df_values = df[['open','close','low','high']].values.tolist()
    df['MA 10'] = ta.SMA(df.close, timeperiod=10)
    df['MA 20'] = ta.SMA(df.close, timeperiod=20)
    df['MA 50'] = ta.SMA(df.close, timeperiod=50)
    df['MA 150'] = ta.SMA(df.close, timeperiod=150)
    df['MA 200'] = ta.SMA(df.close, timeperiod=200)
    sma10 = df['MA 10'].tolist()
    sma20 = df['MA 20'].tolist()
    sma50 = df['MA 50'].tolist()
    sma150 = df['MA 150'].tolist()
    sma200 = df['MA 200'].tolist()

    ticker = df.code[0]

    # 时间戳
    timelist = df.date.tolist()
    # 交易量
    # volumelist = df.volume.tolist()
    volumelist = []
    df.pctChg = df.pctChg.astype(float)
    for i in range(len_):
        if df.pctChg.loc[i] < 0:
            date = [i, df.volume.loc[i], -1]
        else:
            date = [i, df.volume.loc[i], 1]
        volumelist.append(date)
    # K线
    Kline = (
        Kline()
        .add_xaxis(xaxis_data = timelist)
        .add_yaxis(
            series_name = "",
            y_axis = df_values,
            # itemstyle_opts = opts.ItemStyleOpts(color='#089981', color0='#f23645'),
            itemstyle_opts=opts.ItemStyleOpts(
                color = "#089981", 
                color0 = "#f23645",
                border_color = "#089981",
                border_color0 = "#f23645"),
        )
        .set_global_opts(
                legend_opts=opts.LegendOpts(
                    is_show=True, pos_left="left"
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(
                        is_show=False,
                        type_="inside",
                        xaxis_index=[0, 1],
                        range_start=98,
                        range_end=100,
                    ),
                    opts.DataZoomOpts(
                        is_show=True,
                        xaxis_index=[0, 1],
                        type_="slider",
                        pos_top="85%",
                        range_start=98,
                        range_end=100,
                    ),
                ],
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    ),
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="axis",
                    axis_pointer_type="cross",
                    background_color="rgba(245, 245, 245, 0.8)",
                    border_width=1,
                    border_color="#ccc",
                    textstyle_opts=opts.TextStyleOpts(color="#000"),
                ),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=False,
                    dimension=2,
                    series_index=5,
                    is_piecewise=True,
                    pieces=[
                        {"value": 1, "color": "#089981"},
                        {"value": -1, "color": "#f23645"},
                    ],
                ),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True,
                    link=[{"xAxisIndex": "all"}],
                    label=opts.LabelOpts(background_color="#777"),
                ),
                brush_opts=opts.BrushOpts(
                    x_axis_index="all",
                    brush_link="all",
                    out_of_brush={"colorAlpha": 0.1},
                    brush_type="lineX",
                ),
            )
    )

    # 简单易懂均线 MA 
    line = (
            Line()
            .add_xaxis(xaxis_data = timelist)
            # .add_yaxis(
            #     series_name="MA10",
            #     y_axis=calculate_ma(day_count=5, data=chart_data),
            #     is_smooth=True,
            #     is_hover_animation=False,
            #     is_symbol_show = False,
            #     linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            #     label_opts=opts.LabelOpts(is_show=False),
            # )
            .add_yaxis(
                series_name = "MA10",
                y_axis = sma10,
                is_smooth = True,
                is_hover_animation = False,
                is_symbol_show = False,
                linestyle_opts = opts.LineStyleOpts(width=1.5),
                label_opts = opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name = "MA20",
                y_axis = sma20,
                is_smooth = True,
                is_hover_animation = False,
                is_symbol_show = False,
                linestyle_opts = opts.LineStyleOpts(width=1.5),
                label_opts = opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name = "MA50",
                y_axis = sma50,
                is_smooth = True,
                is_hover_animation = False,
                is_symbol_show = False,
                linestyle_opts = opts.LineStyleOpts(width=1.5),
                label_opts = opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name = "MA150",
                y_axis = sma150,
                is_smooth = True,
                is_hover_animation = False,
                is_symbol_show = False,
                linestyle_opts = opts.LineStyleOpts(width=1.5),
                label_opts = opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name = "MA200",
                y_axis = sma200,
                is_smooth = True,
                is_hover_animation = False,
                is_symbol_show = False,
                linestyle_opts = opts.LineStyleOpts(width=1.5),
                label_opts = opts.LabelOpts(is_show=False),
            )
            # .add_yaxis(
            #     series_name="MA150",
            #     y_axis=calculate_ma(day_count=20, data=chart_data),
            #     is_smooth=True,
            #     is_hover_animation=False,
            #     is_symbol_show = False,
            #     linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            #     label_opts=opts.LabelOpts(is_show=False),
            # )
            # .add_yaxis(
            #     series_name="MA200",
            #     y_axis=calculate_ma(day_count=30, data=chart_data),
            #     is_smooth=True,
            #     is_hover_animation=False,
            #     is_symbol_show = False,
            #     linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            #     label_opts=opts.LabelOpts(is_show=False),
            # )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    grid_index=1,
                    axislabel_opts=opts.LabelOpts(is_show=False),
                ),
                yaxis_opts=opts.AxisOpts(
                    grid_index=1,
                    split_number=3,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=True),
                ),
            )
        )

    # 交易量 volume
    bar = (
            Bar()
            .add_xaxis(xaxis_data = timelist)
            .add_yaxis(
                series_name="Volume",
                # 交易量
                y_axis=volumelist,
                xaxis_index=1,
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(
                color = "#73caff", 
                color0 = "#089981",),
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    is_scale=True,
                    grid_index=1,
                    boundary_gap=False,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    split_number=20,
                    min_="dataMin",
                    max_="dataMax",
                ),
                yaxis_opts=opts.AxisOpts(
                    grid_index=1,
                    is_scale=True,
                    split_number=2,
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )

    # Kline And Line
    overlap_kline_line = Kline.overlap(line)

    # Grid Overlap + Bar
    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width="1000px",
            height="800px",
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )

    grid_chart.add_js_funcs("var barData = {}".format(timelist))

    grid_chart.add(
        overlap_kline_line,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
    )
    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="63%", height="16%"
        ),
    )

    grid_chart.render("{}.html".format(ticker))
    # grid_chart.render_notebook()
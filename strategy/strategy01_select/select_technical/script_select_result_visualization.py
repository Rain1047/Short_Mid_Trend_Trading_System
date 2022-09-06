import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
# plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots

price_engine = create_engine('sqlite:///./././datatset/us/us_ticker_seven_year_price.db')
# result_engine = create_engine('sqlite:///strategy\strategy01_select\select_technical\select_test_result\select_test_result.db')
result_engine = create_engine('sqlite:///strategy/strategy01_select/select_technical/select_test_result/select_test_result.db')
# strategy/strategy01_select/select_technical/select_test_result/select_test_result.db
def get_test_result_plot(target_date):
    df = pd.read_sql('{}_test_res'.format(target_date),con=result_engine)
    df=df[df.apply(np.sum,axis=1)!=0]
    df.rename(columns={'declince_avg_90':'decline_avg_90'},inplace=True)

    labels = ['5%~10%', '0~5%', '10%~15%', '15%~20%', '>20%']
    colors = ['#AADEA4','#E7F598','#66C1A4','#3287BD','#235e84']
    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=[df.query('profit_avg_60 < 0.05').index.__len__(), df.query('0.05 < profit_avg_60 < 0.1').index.__len__(), df.query('0.1 < profit_avg_60 <= 0.15').index.__len__(), df.query('0.15 < profit_avg_60 <= 0.2').index.__len__(), df.query('0.2 < profit_avg_60').index.__len__()], name="60 Day Profit"),
                1, 1)
    fig.add_trace(go.Pie(labels=labels, values=[df.query('profit_avg_90 < 0.05').index.__len__(), df.query('0.05 < profit_avg_90 < 0.1').index.__len__(), df.query('0.1 < profit_avg_90 <= 0.15').index.__len__(), df.query('0.15 < profit_avg_90 <= 0.2').index.__len__(), df.query('0.2 < profit_avg_90').index.__len__()], name="90 Day Profit"),
                1, 2)
    fig.add_trace(go.Pie(labels=labels, values=[df.query('profit_avg_120 < 0.05').index.__len__(), df.query('0.05 < profit_avg_120 < 0.1').index.__len__(), df.query('0.1 < profit_avg_120 <= 0.15').index.__len__(), df.query('0.15 < profit_avg_120 <= 0.2').index.__len__(), df.query('0.2 < profit_avg_120').index.__len__()], name="120 Day Profit"),
                1, 3)
    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    
    fig.update_layout(
        title_text='{} 60/90/120 Days Profit Rate Distribution'.format(target_date),
        title_font_size=25,
        title_x=0.5,
        width=1200,
        # title_xanchor='auto',
        paper_bgcolor="#f7fdf7",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='60 Day', x=0.11, y=0.5, font_size=20, showarrow=False),
                    dict(text='90 Day', x=0.5, y=0.5, font_size=20, showarrow=False),
                    dict(text='120 Day', x=0.90, y=0.5, font_size=20, showarrow=False)])

    fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000',width=2)))
    fig.show()

    if not os.path.exists("select_result_visualization"):
        os.mkdir("select_result_visualization")
    fig.write_image("select_result_visualization/{}_plot.png".format(target_date),engine='auto')

    print('Done')
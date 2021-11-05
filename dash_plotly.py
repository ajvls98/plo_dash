# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
import openpyxl
import os
import dash_table
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolValidator
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


app = dash.Dash(__name__)
app2 = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
import glob


targetPattern = r"exec/*.xlsx"
gl = glob.glob(targetPattern)

x = [pd.read_excel(i) for i in gl]
pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)

#메인 데이터프레임
main_df = pd.concat(x, ignore_index=True)
main_df = main_df.sort_values(by=['개찰시간'])
main_df = main_df.drop_duplicates(['학교이름', '개찰시간', '기초가격', '낙찰예정가격', '낙찰방식', '낙찰자']) 
낙찰률_출현빈도 = main_df["낙찰률"].value_counts().rename_axis('낙찰률').reset_index(name='counts')
낙찰자_출현빈도 = main_df["낙찰자"].value_counts().rename_axis('낙찰자').reset_index(name='counts')
df_sort = main_df.sort_values(by=["낙찰자", "낙찰률"], ascending=[True, False])

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

def bar(df, a, b, title_name, width, height, ori=None):
    trace2 = go.Bar(x=df[a], y=df[b], orientation=ori)
    data = [trace2]
    layout = go.Layout(title=title_name)
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        autosize=False,
        width=width,
        height=height,)
    return fig

# 학교  = ""
# def SetColor(x):
#     if(x == 학교):
#         return "red"
#     else:
#         return "green"










app.layout = html.Div(children=[
    html.H1(
        children="안농?"
    
    ),
    html.Div(
        dcc.Graph(
        id='example-graph-2',
        figure=bar(낙찰률_출현빈도, "낙찰률", "counts",'낙찰률 출현빈도', 1600, 800)
    )
    ),
    html.Div(
        dcc.Graph(
        id='example-graph-3',
        figure=bar(낙찰자_출현빈도,"counts", "낙찰자",'낙찰자 출현빈도', 1600, 800,ori="h")
    )
    ),
    html.Div(
    dash_table.DataTable(
    id = 'table',
    columns=[
        {'name': '학교이름', 'id': '학교이름', 'type': 'numeric'},
        {'name': '낙찰률', 'id': '낙찰률', 'type': 'numeric'},
        {'name': '개찰시간', 'id': '개찰시간', 'type': 'datetime'},
        {'name': '낙찰자', 'id': '낙찰자', 'type': 'text'},
        
    ],
    
    data=df_sort.to_dict('records'),
    filter_action='native',
    style_table={
        'height': '600px',
        'width': '100%',
        'overflowY': 'auto',
    },
    
        ),
    ),
       
    
])


if __name__ == '__main__':
    app.run_server(debug=True)
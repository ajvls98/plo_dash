# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
import openpyxl
import os

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



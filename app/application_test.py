# from flask import Flask
# application = Flask(__name__)


# @application.route('/')
# def hello_world():
#     return 'Hello, World!'

import dash
import dash_bootstrap_components as dbc
from dash_core_components.RadioItems import RadioItems
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
# from ipdb import set_trace as st
from datetime import date, datetime, timedelta
# import flask


from Templates.time_slider_graph import create_time_slider_graph


TICKER_CSV_FILE = "./s_and_p_500_tickers/constituents_csv.csv"
TICKER_NAMES_DF = pd.read_csv(TICKER_CSV_FILE)
TICKER_NAMES_DICT = {
    k: v for k, v in zip(
        TICKER_NAMES_DF["Symbol"], TICKER_NAMES_DF["Name"]
    )
}

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    # server=server
    )

application = app.server

app.layout = dbc.Container(
        html.H1("Hello! Plotly!_v7")
    )


if __name__ == "__main__":
    application.run_server(debug=False, host="0.0.0.0", port=8050)

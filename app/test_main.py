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


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    # server=server
    )

server = app.server

app.layout = dbc.Container(
        html.H1("Hello World!")
    )

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8050)

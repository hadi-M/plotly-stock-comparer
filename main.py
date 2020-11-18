from os import name
from threading import main_thread
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
# import pandas as pd
from ipdb import set_trace as st

# from Templates.create_time_slider_graph import create_time_slider_graph
# from callbacks.c1 import c1
from Templates.time_slider_graph import create_time_slider_graph
# Load data
# df = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
# df.columns = [col.replace("AAPL.", "") for col in df.columns]
fig = create_time_slider_graph(None)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY]
    )
# st()


app.layout = dbc.Container(
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="g1", figure=fig),
                width=12            
            )
        )
    )

# c1(df)


if __name__ == "__main__":
    app.run_server(debug=True)

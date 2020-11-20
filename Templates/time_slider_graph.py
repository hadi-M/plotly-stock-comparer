from os.path import join
import plotly.graph_objects as go
from os import listdir
from os.path import join as path_join
import pandas as pd
from ipdb import set_trace as st


def create_time_slider_graph(df):
    # Create figure
    fig = go.Figure()

    # for csv_file in listdir("data"):
    #     temp_df = pd.read_csv(path_join("data", csv_file))
    #     fig.add_trace(
    #         go.Scatter(x=list(temp_df.Date), y=list(temp_df.High))
    #     )
    print(df.columns)
    for ticker in df.columns:
        fig.add_trace(
            go.Scatter(x=df.index, y=df[ticker], name=ticker)
        )

    # Set title
    fig.update_layout(
        title_text="Stock selection dashboard"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(
                        count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"
                    ),
                    dict(
                        count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"
                    ),
                    dict(
                        count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"
                    ),
                    dict(
                        count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"
                    ),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    return fig
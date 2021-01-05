from logging import disable
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
# import os
# print("listdir():", os.listdir())

from Templates.time_slider_graph import create_time_slider_graph

TICKER_CSV_FILE = "./s_and_p_500_tickers/constituents_csv.csv"
TICKER_NAMES_DF = pd.read_csv(TICKER_CSV_FILE)
TICKER_NAMES_DICT = {
    k: v for k, v in zip(
        TICKER_NAMES_DF["Symbol"], TICKER_NAMES_DF["Name"]
    )
}


# Read market data
df = pd.read_pickle(r"data/2020-11-17_market_data_forward_filled.pckl")
df = df
# Create a primary chart so it is not empty
fig = create_time_slider_graph(df.loc[:, "Adj Close"].loc[:, ["AAPL"]])

values_list = df.index.to_series().dt.strftime(r"%Y-%m-%d").reset_index(drop=True)
values_list = values_list.reset_index()

temp_df = df.index.to_series().dt.strftime(r"%Y").reset_index(drop=True).reset_index()
temp_df["Date"] = temp_df["Date"].astype(int)
reverse_marks_dict = temp_df[temp_df["Date"] % 5 == 0].groupby("Date").first().to_dict()["index"]
marks_dict = {v: str(k) for k, v in reverse_marks_dict.items()}
# st()
######
# server = flask.Flask(__name__) #

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    # server=server
    )

application = app.server

app.layout = dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id="graph_output", figure=fig),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                            {
                                "label": f"{ticker} - {name}", "value": ticker
                            } for ticker, name in TICKER_NAMES_DICT.items()
                        ],
                        id="ticker_dp",
                        value=["AAPL"],
                        multi=True
                    ),
                    width=12
                ),
                style={"margin-bottom": "20px"}
            ),

            dbc.CardDeck(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Visualization Tools", style={
                                    "text-align": "center",
                                    "margin-bottom": "20px"
                                    }
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4("Adjust/Not adjust", style={"text-align": "center"}),
                                                dbc.RadioItems(
                                                    options=[
                                                        {'label': 'Adjusted prices', 'value': 'yes'},
                                                        {'label': 'Not adjusted prices', 'value': 'no'},
                                                    ],
                                                    value='no',
                                                    id="radio_adjdusted"
                                                )
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(
                                            [
                                                html.H4("Tickers have their own trend/Start from 100", style={"text-align": "center"}),
                                                dbc.RadioItems(
                                                    options=[
                                                        {'label': 'All start from 100', 'value': '100'},
                                                        {'label': 'All have their own trend', 'value': 'normal'},
                                                    ],
                                                    value='normal',
                                                    id="radio_100"
                                                ),
                                            ],
                                            width=6,
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(

                                            [
                                                html.H4("Date Range", style={"text-align": "center"}),
                                                dcc.DatePickerRange(
                                                    start_date=date(2018, 1, 1),
                                                    end_date=date(2019, 1, 1),
                                                    id="visualization_date_range",
                                                    display_format='DD/MM/YYYY',
                                                    disabled=True
                                                ),
                                            ],
                                            width=12,
                                        )
                                    ],
                                    style={
                                        "margin-top": "20px",
                                        "text-align": "center"
                                    }
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        dcc.RangeSlider(
                                            id='visualization_date_range_slider',
                                            # marks={i: '{}'.format(10 ** i) for i in range(4)},
                                            min=0,
                                            max=len(values_list),
                                            value=[0, len(values_list)-1],
                                            dots=False,
                                            step=1,
                                            # step=timedelta(days=1),
                                            marks=marks_dict,
                                            # marks={
                                            #     1: "1-1-1",
                                            #     5: "5",
                                            #     10: "10",
                                            #     15: "11s5",
                                            #     20: "20"
                                            # },
                                            updatemode='drag'
                                        ),
                                    )
                                )
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Get N highest performing stocks", style={
                                    "text-align": "center",
                                    "margin-bottom": "20px"
                                    }
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4("search on Adjusted/Not adjusted", style={"text-align": "center"}),
                                                dbc.RadioItems(
                                                    options=[
                                                        {'label': 'Adjusted prices', 'value': 'yes'},
                                                        {'label': 'Not adjusted prices', 'value': 'no'},
                                                    ],
                                                    value='no',
                                                    id="radio_adjdusted_get_best"
                                                )
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(
                                            [
                                                html.H4("Number of best stocks to get", style={"text-align": "center"}),
                                                dbc.Input(type="number", id="N_input", min=1, step=1, value=1),
                                            ],
                                            width=6,
                                        )
                                    ],
                                    style={"margin-top": "20px"}
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        [
                                            html.H4("Set dates to get the best stocks in", style={"text-align": "center"}),
                                            dcc.DatePickerRange(
                                                start_date=date(2018, 1, 1),
                                                end_date=date(2019, 1, 1),
                                                id="d1",
                                                display_format='DD/MM/YYYY',
                                                disabled=True
                                            ),
                                            # dcc.RangeSlider(
                                            #     id='non-linear-range-slider',
                                            #     # marks={i: '{}'.format(10 ** i) for i in range(4)},
                                            #     min=1,
                                            #     max=20,
                                            #     value=[3, 10],
                                            #     dots=False,
                                            #     step=0.1,
                                            #     # step=timedelta(days=1),
                                            #     marks={
                                            #         1: "1",
                                            #         5: "5",
                                            #         10: "10",
                                            #         15: "15",
                                            #         20: "20"
                                            #     },
                                            #     updatemode='drag'
                                            # ),
                                            dcc.RangeSlider(
                                                id='d1_date_range_slider',
                                                # marks={i: '{}'.format(10 ** i) for i in range(4)},
                                                min=0,
                                                max=len(values_list),
                                                value=[0, len(values_list)-1],
                                                dots=False,
                                                step=1,
                                                # step=timedelta(days=1),
                                                marks=marks_dict,
                                                # marks={
                                                #     1: "1-1-1",
                                                #     5: "5",
                                                #     10: "10",
                                                #     15: "11s5",
                                                #     20: "20"
                                                # },
                                                updatemode='drag'
                                            ),
                                        ],
                                        width=12,
                                    ),
                                    style={
                                        "margin-top": "20px",
                                        "text-align": "center"
                                    },
                                    justify="center"
                                ),
                                dbc.Row([
                                        dbc.Col(
                                            [
                                                dbc.Button(children="Get", id="get_best_btn", color="primary", block=True),
                                            ],
                                            width=6,

                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Button(children="Apply dates to graph", id="apply_dates_to_visualization", color="primary", block=True),
                                            ],
                                            width=6,

                                        ),
                                    ],
                                    style={"margin-top": "20px"},
                                    # justify="center"
                                )
                            ]
                        )
                    ),
                ]
            )
        ],
    )


@app.callback(
    [
        Output(component_id="graph_output", component_property="figure"),
    ],
    [
        Input(component_id="ticker_dp", component_property="value"),
        Input(component_id="visualization_date_range", component_property="end_date"),
        Input(component_id="visualization_date_range", component_property="start_date"),
        Input(component_id="radio_100", component_property="value"),
        Input(component_id="radio_adjdusted", component_property="value"),
    ],
    prevent_initial_call=True,
)
def update_my_graph(ticker_list, end_date, start_date, normal_or_100, adjusted_or_no):
    """
    Updates the graph on any change of 
    """
    def column_to_normalized(column: pd.Series) -> pd.Series:
        """
        Will change all of the tickers as they have started from 100
        """
        # get first non nan price
        # st()
        first_non_nan_index = column.first_valid_index()
        first_non_nan_value = column.loc[first_non_nan_index]
        return column / first_non_nan_value * 100

    start_date = datetime.strptime(start_date, r"%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, r"%Y-%m-%d").date()
    print(ticker_list)

    if adjusted_or_no == "no":
        new_df = df.loc[start_date:end_date, "Close"].loc[:, ticker_list]
    elif adjusted_or_no == "yes":
        new_df = df.loc[start_date:end_date, "Adj Close"].loc[:, ticker_list]
    # df.loc[start_date + timedelta(days=1):end_date, "Adj Close"].loc[:, ticker_list]
    # st()
    if normal_or_100 == "normal":
        return [create_time_slider_graph(new_df)]
    elif normal_or_100 == "100":
        new_df = new_df.apply(column_to_normalized, axis="index")
        return [create_time_slider_graph(new_df)]

# ## Python version ## 
# @app.callback(
#     [
#         Output(component_id="get_best_btn", component_property="children"),
#     ],
#     [
#         Input(component_id="N_input", component_property="value"),
#     ],
# )
# def update_get_n_best_button(N):
#     return [f"Get best {N} tickers"]

# ## JavaScript version ## #
app.clientside_callback(
    """
    function(N) {
        return "Get best " + String(N) + " tickers";
    }
    """,
    Output(component_id="get_best_btn", component_property="children"),
    [Input(component_id="N_input", component_property="value")],
)


@app.callback(
    [
        Output(component_id="ticker_dp", component_property="value"),
    ],
    [
        Input('get_best_btn', 'n_clicks'),
    ],
    [
        State(component_id="N_input", component_property="value"),
        State(component_id="d1", component_property="start_date"),
        State(component_id="d1", component_property="end_date"),
        State(component_id="radio_adjdusted_get_best", component_property="value"),

    ],
    prevent_initial_call=True,
)
def update_get_n_best_button(n_clicks, N, start_date, end_date, adjustd_or_no):
    # st()
    if adjustd_or_no == "no":
        best_tickers = df.loc[start_date: end_date, "Close"].apply(lambda x: x[-1]/x[0], axis="index").nlargest(N).index.to_list()
        return [best_tickers]
    elif adjustd_or_no == "yes":
        best_tickers = df.loc[start_date: end_date, "Adj Close"].apply(lambda x: x[-1]/x[0], axis="index").nlargest(N).index.to_list()
        return [best_tickers]


@app.callback(
    [
        Output(component_id="visualization_date_range_slider", component_property="value"),
    ],
    [
        Input('apply_dates_to_visualization', 'n_clicks'),
    ],
    [
        State(component_id="d1_date_range_slider", component_property="value"),
    ],
    prevent_initial_call=True,
)
def apply_best_dates_to_visulization_dates(n_clicks, dates):
    return [dates]


@app.callback(
    [
        Output(component_id="d1_date_range_slider", component_property="value"),
    ],
    [
        Input(component_id="d1", component_property="start_date"),
        Input(component_id="d1", component_property="end_date"),
    ],
)
def digitrange_to_daterange(start_date, end_date):
    # value0 = values_list[values_list <= start_date].iloc[-1]
    # value1 = values_list[values_list >= end_date].iloc[0]
    # st()
    value0 = values_list[values_list["Date"] == start_date]["index"].iloc[0]
    value1 = values_list[values_list["Date"] == end_date]["index"].iloc[0]
    # value0 = values_list[values_list == start_date].index[0]
    # value1 = values_list[values_list == end_date].index[0]
    return [[value0, value1]]


@app.callback(
    [
        Output(component_id="d1", component_property="start_date"),
        Output(component_id="d1", component_property="end_date"),
    ],
    [
        Input(component_id="d1_date_range_slider", component_property="value"),
    ],
)
def daterange_to_digitrange(value):
    print("1")
    # return [values_list.iloc[value[0]], values_list.iloc[value[1]]]
    # st()
    return [values_list.iloc[value[0]]["Date"], values_list.iloc[value[1]]["Date"]]


@app.callback(
    [
        Output(component_id="visualization_date_range", component_property="start_date"),
        Output(component_id="visualization_date_range", component_property="end_date"),
    ],
    [
        Input(component_id="visualization_date_range_slider", component_property="value"),
    ],
)
def daterange_to_digitrange(value):
    print("2")
    # return [values_list.iloc[value[0]], values_list.iloc[value[1]]]
    # st()
    return [values_list.iloc[value[0]]["Date"], values_list.iloc[value[1]]["Date"]]


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)

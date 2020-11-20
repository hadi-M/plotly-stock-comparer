from os import POSIX_FADV_NORMAL, name
from threading import main_thread
import dash
import dash_bootstrap_components as dbc
from dash_core_components.RadioItems import RadioItems
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
from ipdb import set_trace as st
from datetime import date, datetime


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

# Create a primary chart so it is not empty
fig = create_time_slider_graph(df.loc[:, "Adj Close"].loc[:, ["AAPL"]])

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY]
    )

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
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.DatePickerRange(
                            start_date=date(2018, 1, 1),
                            end_date=date(2019, 1, 1),
                            id="date_range",
                            display_format='DD/MM/YYYY',
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.RadioItems(
                            options=[
                                {'label': 'All start from 100', 'value': '100'},
                                {'label': 'All have their own trend', 'value': 'normal'},
                            ],
                            value='normal',
                            id="radio_100"
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.RadioItems(
                            options=[
                                {'label': 'Adjusted prices', 'value': 'yes'},
                                {'label': 'Not adjusted prices', 'value': 'no'},
                            ],
                            value='no',
                            id="radio_adjdusted"
                        ),
                        width=3
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                html.P(
                                    "Get N highest performing stocks between certain dates"
                                )
                            ),
                            dbc.Row(
                                dbc.Input(type="number", id="N_input", min=1, step=1, value=1),
                            ),
                            dbc.Row(
                                dbc.Button(children="Get", id="get_best_btn", color="primary"),
                            ),
                        ]
                    )
                ]
            ),
        
        


            # dbc.CardDeck(
            #     [
            #         dbc.Card(
            #             dbc.CardBody(
            #                 [
            #                     dbc.Row(
            #                         [
            #                             dbc.Col(
            #                                 dcc.DatePickerRange(
            #                                     start_date=date(2018, 1, 1),
            #                                     end_date=date(2019, 1, 1),
            #                                     id="s1",
            #                                     display_format='DD/MM/YYYY',
            #                                 ),
            #                             width=6,
            #                             ),
            #                             dbc.Col(
            #                                 dcc.DatePickerRange(
            #                                     start_date=date(2018, 1, 1),
            #                                     end_date=date(2019, 1, 1),
            #                                     id="s2",
            #                                     display_format='DD/MM/YYYY',
            #                                 ),
            #                             width=6,
            #                             )
            #                         ]
            #                     )
            #                 ]
            #             )
            #         ),
            #         dbc.Card(
            #             dbc.CardBody(
            #                 [
            #                     html.H5("Card 2", className="card-title"),
            #                     html.P(
            #                         "This card has some text content.",
            #                         className="card-text",
            #                     ),
            #                     dbc.Button(
            #                         "Click here", color="warning", className="mt-auto"
            #                     ),
            #                 ]
            #             )
            #         ),
            #     ]
            # )


        ],



    )


@app.callback(
    [
        Output(component_id="graph_output", component_property="figure"),
    ],
    [
        Input(component_id="ticker_dp", component_property="value"),
        Input(component_id="date_range", component_property="end_date"),
        Input(component_id="date_range", component_property="start_date"),
        Input(component_id="radio_100", component_property="value"),
        Input(component_id="radio_adjdusted", component_property="value"),
    ],
)
def update_my_graph(ticker_list, end_date, start_date, normal_or_100, adjustd_or_no):
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

    if adjustd_or_no == "no":
        new_df = df.loc[start_date:end_date, "Close"].loc[:, ticker_list]
    elif adjustd_or_no == "yes":
        new_df = df.loc[start_date:end_date, "Adj Close"].loc[:, ticker_list]

    if normal_or_100 == "normal":
        return [create_time_slider_graph(new_df)]
    elif normal_or_100 == "100":
        new_df = new_df.apply(column_to_normalized, axis="index")
        return [create_time_slider_graph(new_df)]


@app.callback(
    [
        Output(component_id="get_best_btn", component_property="children"),
    ],
    [
        Input(component_id="N_input", component_property="value"),
    ],
)
def update_get_n_best_button(N):
    return [f"Get best {N} tickers"]


@app.callback(
    [
        Output(component_id="ticker_dp", component_property="value"),
    ],
    [
        Input('get_best_btn', 'n_clicks'),
    ],
    [
        State(component_id="N_input", component_property="value"),
        State(component_id="date_range", component_property="start_date"),
        State(component_id="date_range", component_property="end_date"),
        State(component_id="radio_adjdusted", component_property="value"),

    ],
    prevent_initial_call=True,
)
def update_get_n_best_button(n_clicks, N, start_date, end_date, adjustd_or_no):
    if adjustd_or_no == "no":
        best_tickers = df.loc[start_date: end_date, "Close"].apply(lambda x: x[-1]/x[0], axis="index").nlargest(N).index.to_list()
        return [best_tickers]
    elif adjustd_or_no == "yes":
        best_tickers = df.loc[start_date: end_date, "Adj Close"].apply(lambda x: x[-1]/x[0], axis="index").nlargest(N).index.to_list()
        return [best_tickers]


if __name__ == "__main__":
    app.run_server(debug=True)

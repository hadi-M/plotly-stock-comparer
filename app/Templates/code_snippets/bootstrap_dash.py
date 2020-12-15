from os import name
from threading import main_thread
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd

from Templates.header import header
from Templates.content import content

df = pd.read_csv("./Berlin_crimes.csv")


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY]
    )

app.layout = html.Div(
    dbc.Container(
        [
            header("Hadi"),
            dbc.Button(df.columns[0], color="success", className="mr-1"),
            dbc.Button("danger", color="danger", className="mr-1"),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button("danger", color="danger", className="mr-1"),
                        # width=4,
                        lg={"size": 3},
                        sm={"size": 12}
                        ),
                    dbc.Col(
                        dbc.Button("danger", color="danger", className="mr-1"),
                        # width=4,
                        lg={"size": 6},
                        sm={"size": 12}
                        ),
                    dbc.Col(
                        dbc.Button("danger", color="danger", className="mr-1"),
                        # width=4,
                        lg={"size": 3},
                        sm={"size": 12}
                        )
                ]
            ),
            content()
        ]
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)

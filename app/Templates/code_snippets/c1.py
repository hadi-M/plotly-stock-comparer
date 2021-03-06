from dash.dependencies import Input, Output, State


def c1(df):
    @app.callback(
        [
            Output(component_id="graph-output", component_property="figure"),
            Output(component_id="my_dp", component_property="value")
        ],
        [
            Input(component_id="dp1", component_property="value")
        ],
    )
    def update_my_graph(val_chosen):
        print(val_chosen)
        if len(val_chosen) > 0:
            dff = df[df["fund_extended_name"].isin(val_chosen)]
            fig = px.pie(dff, values="ytd_return", names="fund_extended_name", title="Year-to-Date Returns")
            fig.update_traces(textinfo="value+percent").update_layout(title_x=0.5)
            return fig, val_chosen
        elif len(val_chosen) == 0:
            raise dash.exceptions.PreventUpdate


    @app.callback(
        Output(component_id="dp1", component_property="value"),
        [Input(component_id="btn1", component_property="n_clicks")],
        prevent_initial_call=True
    )
    def clear_dp1(n):
        return []
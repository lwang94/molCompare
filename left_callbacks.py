from dash import Output, Input, State, callback, ctx
from dash.dash_table.Format import Format, Scheme, Trim

import pandas as pd
import plotly.graph_objects as go

import util
import left_callbacks_util as lcu


def callbacks_left(app):

    @callback(
        Output('graph', 'figure', allow_duplicate=True),
        Output('clicks', 'data', allow_duplicate=True),
        Input('og_graph', 'data'),
        Input('graph', 'clickData'),
        Input('full_table', 'selected_rows'),
        State('graph_option', 'value'),
        State('full_table', 'data'),
        State('full_table', 'selected_columns'),
        State('clicks', 'data'),
        State('index_map', 'data'),
        prevent_initial_call=True
    )
    def pick_datapoint(fig, click, rows, value, data, columns, clicked_points, index_map):    
        if value == 'Histogram':
            fig, clicked_points = lcu.pick_datapoint_histogram(
                data,
                rows,
                columns,
                fig,
                clicked_points,
                ctx.triggered_id,
                click,
                index_map
            )
        else:
            fig, clicked_points = lcu.pick_datapoint_scatter(
                data, 
                rows,
                columns,
                fig,
                clicked_points,
                ctx.triggered_id,
                index_map,
                click
            )
        return fig, clicked_points



    @callback(
        [
            Output('og_graph', 'data'),
            Output('clicks', 'data'),
            Output('index_map', 'data'),
            Output('full_table', 'selected_columns', allow_duplicate=True)
        ],
        Input('full_table', 'derived_filter_query_structure'),
        Input('full_table', 'selected_columns'),
        Input('full_table', 'data'),
        Input('graph_option', 'value'),
        prevent_initial_call=True
    )
    def create_graph(query, col, data, option):
        df = pd.DataFrame(data)
        if query is not None:
            query_string, df = util.construct_filter(query, df)
            if query_string != '':
                df = df.query(query_string)
            index_map = {i: df.iloc[i, 0] for i in range(len(df.index))}
        else:
            index_map = None

        num_unique = df[col[0]].nunique()
        if option == "Histogram":
            fig = go.Figure(data=go.Histogram(x=df[col[0]], marker={'color': 'blue'}))
            col = [col[0]]
        else:
            if len(col) < 2:
                fig = go.Figure(go.Scatter(
                    x=[0],
                    y=[0],
                    mode="markers+text",
                    marker={'color': 'blue'},
                    text=["Please select x and y columns"],
                    textposition="top center" 
                ))
                return fig, {'Histogram': ([], num_unique), 'Scatter': []}, index_map, col
            if len(col) > 2:
                col = col[-2:]
            fig = go.Figure(
                data=go.Scatter(
                    x=df[col[0]], 
                    y=df[col[1]],
                    mode='markers', 
                    marker={'color': 'blue'}
                ),
                layout={'xaxis_title': col[0], 'yaxis_title': col[1]}
            )
        fig.update_layout(margin={'l': 10, 'r': 10, 'b': 10, 't': 10}, showlegend=False)

        return (
            fig, 
            {
                'Histogram': {'points': {}, 'num_unique': num_unique}, 
                'Scatter': {}
            }, 
            index_map, 
            col
        )


    @callback(
        [
            Output('full_table', 'data'),
            Output('full_table', 'columns'),
            Output('filtered_table', 'columns'),
            Output('full_table', 'column_selectable'),
            Output('full_table', 'tooltip_data')
        ],
        Input('graph_option', 'value'),
        Input('smiles_data', 'children')
    )
    def populate_full_table(val, children):
        data = children['props']['data'][0]

        if val == 'Histogram':
            column_selectable = 'single'
        else:
            column_selectable = 'multi'

        initial_columns = [
            {'name': 'index', 'id': 'index', 'selectable': False},
            {'name': 'SMILES', 'id': 'SMILES', 'selectable': False},
            {'name': 'Cluster', 'id': 'Cluster', 'selectable': True}
        ]
        desc_columns = [
            {
                'name': col, 
                'id': col, 
                'selectable': True, 
                'type': 'numeric', 
                'format': Format(precision=2, scheme=Scheme.fixed, trim=Trim.yes)
            } 
            for col in children['props']['data'][1][3:]
        ]
        columns = initial_columns + desc_columns

        tooltip_data = [
            {'SMILES': row['SMILES']}
            for row in data
        ]

        return data, columns, columns, column_selectable, children['props']['data'][2]
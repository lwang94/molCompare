from dash import html, dcc, dash_table, Output, Input, State, callback, ctx
from dash_extensions.enrich import DashProxy, BlockingCallbackTransform
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML as dhtml
from dash.dash_table.Format import Format, Scheme, Trim

import base64
import io
import os

import pandas as pd
import plotly.graph_objects as go
from rdkit import Chem

import util
import time


app = DashProxy(transforms=[BlockingCallbackTransform(timeout=5)])

app.layout = html.Div([
    html.Div(
        children=[
            dcc.Upload(
                id='upload_data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.Button('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                }
            ),
            dcc.Loading(
                id='loading',
                type='default',
                style={'margin-top': '50px'},
                children=[html.Div(id='smiles_data')]
            )
        ],
        className='one row'       
    ),
    html.Div(
        children=[
            dcc.RadioItems(
                id='graph_option',
                options=['Histogram', 'Scatter'],
                value='Histogram',
                inline=True,
                style={
                    'margin-top': 10,
                    'magin-bot': 5
                }
            ),
            dcc.Store(id='og_graph'),
            dcc.Graph(
                id='graph',
                style={'margin-top': '50px'}
            ),
            dcc.Store(id='clicks'),
            dash_table.DataTable(
                id='full_table',
                row_selectable='multi',
                selected_columns=['Cluster'],
                filter_action='native',
                page_size=50,
                style_data_conditional=[{
                    'if': {'column_id': 'SMILES'},
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0
                }],
                style_table={
                    'height': '300px',
                    'overflowY': 'auto' 
                },
                tooltip_duration=None,
                css=[{
                    'selector': '.dash-table-tooltip',
                    'rule': """
                        background-color: black;
                        width: fit-content; 
                        max-width: unset;
                        color: white
                    """
                }]
            )
        ],
        className='six columns'
    ),
    html.Div(
        children=[
            html.Div(id='mol_grid'),
            dash_table.DataTable(
                id='filtered_table',
                row_selectable='multi',
                filter_action='native',
                page_size=50,
                style_data_conditional=[{
                    'if': {'column_id': 'SMILES'},
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0
                }],
                style_table={
                    'height': '300px',
                    'overflowY': 'auto' 
                },
                tooltip_duration=None,
                css=[{
                    'selector': '.dash-table-tooltip',
                    'rule': """
                        background-color: black;
                        width: fit-content; 
                        max-width: unset;
                        color: white
                    """
                }]
            )
        ],
        className='six columns'
    )
])


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
    prevent_initial_call=True
)
def pick_datapoint(fig, click, rows, value, data, columns, clicked_points):    
    if value == 'Histogram':
        if rows is not None:
            x_vals = set([data[row][columns[0]] for row in rows])
            fig['layout']['shapes'] = []
            for x in x_vals:
                fig['layout']['shapes'].append({
                    'line': {'color': 'red'},
                    'type': 'line',
                    'x0': x,
                    'x1': x,
                    'xref': 'x',
                    'y0': 0,
                    'y1': 1,
                    'yref': 'y domain'
                })
        clicked_points['Histogram'][0] = set(clicked_points['Histogram'][0])
        if ctx.triggered_id == 'graph':
            if click['points'][0]['binNumber'] in clicked_points['Histogram'][0]:
                clicked_points['Histogram'][0].remove(click['points'][0]['binNumber'])
            else:
                clicked_points['Histogram'][0].add(click['points'][0]['binNumber'])
        colors = []
        for i in range(clicked_points['Histogram'][1]):
            if i in clicked_points['Histogram'][0]:
                colors.append('red')
            else:
                colors.append('blue')

        fig['data'][0]['marker'] = {'color': colors}
        clicked_points['Histogram'][0] = list(clicked_points['Histogram'][0])
    else:
        if len(columns) < 2:
            return fig, clicked_points
        else:
            clicked_points['Scatter'] = {
                tuple(point) for point in clicked_points['Scatter']
            }
            if ctx.triggered_id == 'graph':
                if (click['points'][0]['x'], click['points'][0]['y']) in clicked_points['Scatter']:
                    clicked_points['Scatter'].remove((
                        click['points'][0]['x'],
                        click['points'][0]['y']
                    ))
                else:
                    clicked_points['Scatter'].add((
                        click['points'][0]['x'],
                        click['points'][0]['y']
                    ))
            point_values = set()
            if rows is not None:
                for row in rows:
                    point_values.add((data[row][columns[0]], data[row][columns[1]]))
            red_points = point_values.update(clicked_points['Scatter'])
            colors = []
            for x, y in zip(fig['data'][0]['x'], fig['data'][0]['y']):
                if (x, y) in point_values:
                    colors.append('red')
                else:
                    colors.append('blue')
            fig['data'][0]['marker'] = {'color': colors}
            clicked_points['Scatter'] = list(clicked_points['Scatter'])
    return fig, clicked_points



@callback(
    [
        Output('og_graph', 'data'),
        Output('clicks', 'data'),
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
            return fig, {'Histogram': ([], num_unique), 'Scatter': []}, col
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

    return fig, {'Histogram': ([], num_unique), 'Scatter': []}, col


@callback(
    [
        Output('full_table', 'data'),
        Output('full_table', 'columns'),
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

    string_column = [
        {'name': 'SMILES', 'id': 'SMILES', 'selectable': False},
        {'name': 'Cluster', 'id': 'Cluster', 'selectable': True}
    ]
    columns = [
        {
            'name': col, 
            'id': col, 
            'selectable': True, 
            'type': 'numeric', 
            'format': Format(precision=2, scheme=Scheme.fixed, trim=Trim.yes)
        } 
        for col in children['props']['data'][1][2:]
    ]
    columns = string_column + columns

    tooltip_data = [
        {'SMILES': row['SMILES']}
        for row in data
    ]

    return data, columns, column_selectable, children['props']['data'][2]


@callback(
    Output('smiles_data', 'children'),
    Input('upload_data', 'contents'),
    Input('upload_data', 'filename')
)
def store_df(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    except:
        return html.Div(
            ['There was an error processing this file'],
            style={'textAlign': 'center'}
        )

    smiles_col = df.columns[0]
    df['mol'] = df[smiles_col].apply(Chem.MolFromSmiles)
    df['Cluster'] = util.butina_cluster(df.mol.values)
    df['desc'] = df['mol'].apply(util.calc_descriptors)
    desc_cols = ['MW', 'LogP', 'NumAromatic', 'HBD', 'HBA']
    df[desc_cols] = df['desc'].to_list()
    df = df.rename(columns={smiles_col: 'SMILES'})
    df = df.drop(columns=['mol', 'desc'])

    return dcc.Store(
        id='smiles_data_store', 
        data=[
            df.to_dict('records'), 
            df.columns,
            [{'SMILES': row} for row in df['SMILES']]
        ]
    )


if __name__ == '__main__':
    app.run(debug=True)
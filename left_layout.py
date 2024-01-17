from dash import html, dcc, dash_table


def left():
    return html.Div(
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
    )
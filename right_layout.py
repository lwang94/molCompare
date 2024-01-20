from dash import html, dcc, dash_table


def right():
    return html.Div(
        children=[
            dcc.Store(id='selected_mol', data=[]),
            html.Div(
                id='mol_grid', 
                style={
                    'border': '2px black solid',
                    'height': '530px',
                    'overflowY': 'scroll'
                }
            ),
            dcc.Store(id='filtered_rows', data=[]),
            dash_table.DataTable(
                id='filtered_table',
                data=[],
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
                row_deletable=True,
                row_selectable='multi',
                css=[{
                    'selector': '.dash-table-tooltip',
                    'rule': """
                        background-color: black;
                        width: fit-content; 
                        max-width: unset;
                        color: white
                    """
                }]
            ),
            html.Button('Reset', id='reset_button')
        ],
        className='six columns'
    )
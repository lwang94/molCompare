from dash import html, dcc, dash_table


def right():
    return html.Div(
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
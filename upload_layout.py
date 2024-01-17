from dash import html, dcc


def upload():
    return html.Div(
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
    )
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

from upload_layout import upload
from left_layout import left
from right_layout import right

from upload_callbacks import callbacks_upload
from left_callbacks import callbacks_left

import right_callbacks_util as rcu


app = DashProxy(transforms=[BlockingCallbackTransform(timeout=5)])

app.layout = html.Div([
    upload(),
    left(),
    right()
])
@callback(
    Output('mol_grid', 'children'),
    Input('filtered_table', 'selected_rows'),
    State('filtered_table', 'data')
)
def populate_mol_grid(rows, data):
    html_rows = []
    new_html_row = []
    r = 0
    for i, row in enumerate(rows):
        if i // 3 > r:
            html_rows.append(new_html_row)
            r += 1
            new_html_row = []
        mol = util.smi2svg(data[row]['SMILES'])
        new_html_row.append(html.Div(
            [dhtml(mol)], 
            className='four columns'
        ))
    html_rows.append(new_html_row)

    children = []
    for html_row in html_rows:
        children.append(html.Div(html_row, className='one row'))
    return children


@callback(
    Output('filtered_table', 'data'),
    Output('filtered_table', 'tooltip_data'),
    Output('filtered_table', 'style_data_conditional'),
    Output('filtered_rows', 'data'),
    Input('clicks', 'data'),
    Input('full_table', 'selected_rows'),
    State('full_table', 'data'),
    State('filtered_rows', 'data'),
    State('graph_option', 'value'),
    State('smiles_data', 'children')
)
def populate_filtered_table(click, rows, data, filtered_rows, value, children):
    if value == 'Histogram':
        res = rcu.populate_filtered_table_histogram(
            data,
            children, 
            rows, 
            click,
            filtered_rows
        )
    else:
        res = rcu.populate_filtered_table_scatter(
            data, 
            children, 
            rows, 
            click, 
            filtered_rows
        )
    return res

        


callbacks_left(app)
callbacks_upload(app)


if __name__ == '__main__':
    app.run(debug=True)
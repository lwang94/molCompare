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


app = DashProxy(transforms=[BlockingCallbackTransform(timeout=5)])

app.layout = html.Div([
    upload(),
    left(),
    right()
])


# @callback(
#     Output('filtered_table', 'data'),
#     Input('graph', 'clickData'),
#     Input('full_table', 'selected_rows'),
#     State('full_table', 'data'),
#     State('graph_option', 'value')
# )
# def populate_filtered_table(click, row, data, value):
#     if value == 'Histogram':
#         if rows is not None:
#             return


callbacks_left(app)
callbacks_upload(app)


if __name__ == '__main__':
    app.run(debug=True)
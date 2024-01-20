from dash import html, Output, Input, State, callback
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML as dhtml

import util
import right_callbacks_util as rcu


def callbacks_right(app):

    @callback(
        Output('mol_grid', 'children'),
        Output('selected_mol', 'data'),
        Input('filtered_table', 'selected_rows'),
        State('filtered_table', 'data')
    )
    def populate_mol_grid(rows, data):
        html_rows = []
        new_html_row = []
        selected_rows = []
        r = 0
        for i, row in enumerate(rows):
            if i // 3 > r:
                html_rows.append(new_html_row)
                r += 1
                new_html_row = []
            mol = util.smi2svg(data[row]['SMILES'])
            selected_rows.append(data[row]['index'])
            new_html_row.append(html.Div(
                [dhtml(mol), data[row]['index']], 
                style={'border': '1px blue solid'},
                className='four columns'
            ))
        html_rows.append(new_html_row)

        children = []
        for html_row in html_rows:
            children.append(html.Div(html_row, className='one row'))
        return children, selected_rows


    @callback(
        Output('filtered_table', 'data'),
        Output('filtered_table', 'tooltip_data'),
        Output('filtered_table', 'style_data_conditional'),
        Output('filtered_table', 'selected_rows'),
        Output('filtered_rows', 'data'),
        Input('clicks', 'data'),
        Input('full_table', 'selected_rows'),
        State('full_table', 'data'),
        State('filtered_rows', 'data'),
        State('graph_option', 'value'),
        State('smiles_data', 'children'),
        State('selected_mol', 'data')
    )
    def populate_filtered_table(click, rows, data, filtered_rows, value, children, selected_mol):
        if value == 'Histogram':
            res = rcu.populate_filtered_table_histogram(
                data,
                children, 
                rows, 
                click,
                filtered_rows,
                set(selected_mol)
            )
        else:
            res = rcu.populate_filtered_table_scatter(
                data, 
                children, 
                rows, 
                click, 
                filtered_rows,
                set(selected_mol)
            )
        return res
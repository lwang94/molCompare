from dash import html, dcc, Output, Input, callback

import base64
import io

import pandas as pd
from rdkit import Chem

import util


def callbacks_upload(app):

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
        df['index'] = df.index
        df = df.rename(columns={smiles_col: 'SMILES'})
        df = df.drop(columns=['mol', 'desc'])
        df = df[['index', 'SMILES', 'Cluster'] + desc_cols]
        return dcc.Store(
            id='smiles_data_store', 
            data=[
                df.to_dict('records'), 
                df.columns,
                [{'SMILES': row} for row in df['SMILES']]
            ]
        )
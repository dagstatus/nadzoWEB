import dash
import dash_auth
import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly
from base_nadzor.app import app
# from base_nadzor.read_db.read_db_func import ReadpandasRNV, SqlDB
from base_nadzor.pdf_rnv_creator import pdf_rnv_make_file
from base_nadzor.read_db import write_db
from base_nadzor.pages import vvod_text
from dash.exceptions import PreventUpdate
import pickle

ReadDBSQL = write_db.WriteDB()

style_data_conditional = [
    {
        "if": {"state": "active"},
        "backgroundColor": "rgba(150, 180, 225, 0.2)",
        "border": "1px solid blue",
    },
    {
        "if": {"state": "selected"},
        "backgroundColor": "rgba(0, 116, 217, .03)",
        "border": "1px solid blue",
    },
]


def read_rnv(uid):
    df = ReadDBSQL.read_rnv_by_uid(uid)
    df = df.rename(index={0: 'РНВ'})

    df = df.T
    df = df.reset_index()

    table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id='table_rnv_editor',
                                 style_data_conditional=style_data_conditional,
                                 editable=True,
                                 # filter_action="native"
                                 )
    return table


layout = html.Div([
    html.H4('Редактирование разрешения на ввод', className="text-center", style={'margin': '20px'}),
    html.Div(id='rnv_editor_div_table', style={'width': '500px', 'margin': 'auto'}),
    html.Div(id='editing-prune-data-output'),
    dbc.Button(id='invisible_button', style={'display': 'none'})
])


@app.callback(
              Output('rnv_editor_div_table', 'children'),
              Input('invisible_button', 'n_clicks'))
def your_function(n_clicks):
    table = ''
    try:
        with open('rnv_editor.txt', 'rb') as f:
            data_new = pickle.load(f)

        uid_ = data_new.get('row').get('uid')

        table = read_rnv(uid=uid_)
    except Exception as ex:
        print(ex)

    return table
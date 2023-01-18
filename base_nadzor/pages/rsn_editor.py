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
from base_nadzor.pages import razr_text
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

def read_rns(uid):
    df = ReadDBSQL.read_rsn_by_uid(uid)
    df = df.rename(index={0: 'РНС'})
    df = df.T
    df = df.drop(['uid', 'date_write_to_db', 'show_flag'])

    df_labels = pd.DataFrame(index=razr_text.rsn_keys, data={'Name': razr_text.rsn_labels_4_editor})

    df = pd.merge(left=df_labels, left_index=True, right=df, right_index=True)

    table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                                 id='table_rns_editor',
                                 style_data_conditional=style_data_conditional,
                                 editable=True,
                                 style_data={'whiteSpace': 'normal', 'height': 'auto'},
                                 style_cell={'maxWidth': '400px', 'minWidth': '400px'},
                                 # filter_action="native"
                                 )
    return table

layout = html.Div([
    dbc.Button("Сохранить изменения", color="success", className="me-1", id='rns_edit_save_btn',
               style={'float': 'auto', 'margin': '20px'}, href="/rns"),
    html.H4('Редактирование разрешения на ввод', className="text-center", style={'margin': '20px'}),
    html.Div(id='rns_editor_div_table', style={'width': '800px', 'margin': 'auto'},
             children=[dash_table.DataTable(id='table_rns_editor')]),
    html.Div(id='editing-prune-data-output_rns'),
    dbc.Button(id='invisible_button_rns', style={'display': 'none'}),
    html.Div(id='editor_invise_div1_rns')
])

@app.callback(
    Output('rns_editor_div_table', 'children'),
    Input('invisible_button_rns', 'n_clicks'))
def update_on_load_editor(n_clicks):
    table = ''
    try:
        with open('rsn_editor.txt', 'rb') as f:
            data_new = pickle.load(f)

        uid_ = data_new.get('row').get('uid')

        table = read_rns(uid=uid_)
    except Exception as ex:
        print(ex)

    return table

@app.callback(
    Output('editor_invise_div1_rns', 'children'),
    Input('rns_edit_save_btn', 'n_clicks'),
    State('table_rns_editor', 'data'))
def save_edit_rnv(n_clicks, data_in):
    if n_clicks is None:
        return ''
    else:
        # print(data_in)
        df_to_save = pd.DataFrame(index=razr_text.rsn_keys, data=data_in)
        df_to_save = df_to_save.T.drop('Name')

        ReadDBSQL.add_rsn_to_sql(df_to_save.to_dict('records')[0])



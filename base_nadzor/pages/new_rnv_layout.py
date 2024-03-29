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

class MemoryRazdels:
    def __init__(self):
        self.col_r6 = 1
        self.col_r7 = 1

        self.click_r6 = 0
        self.click_r7 = 0

        self.name_id_rnv = []

MemoryRazdelsObj = MemoryRazdels()

WriteRSNObj = write_db.WriteDB()


def make_layout_razdels_rnv(objects_6=1, objects_7=1):
    rnv_div = []

    if MemoryRazdelsObj.col_r6 > objects_6:
        objects_6 = MemoryRazdelsObj.col_r6
    else:
        MemoryRazdelsObj.col_r6 = objects_6

    if MemoryRazdelsObj.col_r7 > objects_7:
        objects_7 = MemoryRazdelsObj.col_r7
    else:
        MemoryRazdelsObj.col_r7 = objects_7

    for idx, razdel in enumerate(vvod_text.rnv_razdels):
        # num_object = 1
        obj_max = 1
        if idx + 1 == 6:
            obj_max = objects_6
        if idx + 1 == 7:
            obj_max = objects_7
        # for num_object in range(1, obj_max+1):
        tmp_razdel = []
        acc_tmp = []

        for label_x in vvod_text.rnv_labels:
            num_razdel = str(razdel)[7]
            if str(label_x).startswith(str(num_razdel)):
                if label_x in vvod_text.rnv_non_input_labels:
                    tmp_razdel.append(
                        dbc.Row([
                            dbc.Col(label_x)
                        ]
                        ))
                else:

                    ############# temp ##############
                    # if 'X' in label_x:
                    #     label_x = label_x.replace('X', '1')

                    if 'X' in label_x:
                        label_x = label_x.replace('X', str(razdel[-1]))

                    tmp_razdel.append(
                        dbc.Row([
                            dbc.Label(label_x, width=10),
                            dbc.Col(dbc.Input(id='rnv' + str(label_x.split()[0][:-1]).replace('.', '_'),
                                              ),
                                    width=10),
                        ], class_name="mb-3")
                    )

                    MemoryRazdelsObj.name_id_rnv.append('rnv' + str(label_x.split()[0][:-1]).replace('.', '_'))

                    # print(str(label_x.split()[0][:-1]))
                    # print(self.edit_dict.get(str(label_x.split()[0][:-1]), ''))
                    razdel_text = razdel
                    if razdel in vvod_text.rnv_razdels_with_x:
                        razdel_text = razdel
                    acc_tmp = dbc.AccordionItem(tmp_razdel, title=razdel_text)
        rnv_div.append(acc_tmp)
        # MemoryRazdelsObj.name_id_rnv = list(set(MemoryRazdelsObj.name_id_rnv))
    return rnv_div


def make_layout_rnv():
    return html.Div([
        html.H4('Новое разрешения на ввод', className="text-center", style={'margin': '10px'}),
        html.Div([
            html.Div([
                dbc.Button("Сохранить", color="success", className="me-1", id='save_new_rnv_to_db',
                           style={'margin': '10px'}, href="/rnv"),

                html.Div([
                    dbc.Button("СБРОСИТЬ", color="danger", className="me-1", id='drop_all_rnv_new',
                               style={'margin': '10px'}),
                    # dbc.Button("Добавить объект в раздел 6", color="warning", className="me-1",
                    #            id='button_rnv_add_obj_r6',
                    #            style={'margin': '10px'}),
                    # dbc.Button("Добавить объект в раздел 7", color="warning", className="me-1",
                    #            id='button_rnv_add_obj_r7',
                    #            style={'margin': '10px'}),
                ], style={'float': 'right'}),
            ]),
            html.Div([], id='rnv_null_update_div'),
            dbc.Accordion(make_layout_razdels_rnv(), start_collapsed=True, id='rnv_razdels_accord'),
            html.Div(id='rnv_null_save_div'),
            html.Div(id='rnv_null_save_di2'),
            html.Div(id='div_rnv_cache', style={'block': 'none'}),
            dcc.Location(id='url_new_rnv_update', refresh=True),
        ])

    ])


layout = make_layout_rnv()


@app.callback(
    Output('url_new_rnv_update', 'href'),
    Input('drop_all_rnv_new', 'n_clicks'),
    prevent_initial_call=True, )
def save_rnv(clicks):
    if clicks is None:
        return ''
    else:
        MemoryRazdelsObj.__init__()
        return '/new_rnv'

# @app.callback(
#     Output('rnv_razdels_accord', 'children'),
#     Input('button_rnv_add_obj_r6', 'n_clicks'),
#     Input('button_rnv_add_obj_r7', 'n_clicks'),
#     prevent_initial_call=True, )
# def add_r6(clicks_r6, clicks_r7):
#     if clicks_r6 is None:
#         if clicks_r7 is None:
#             return ''
#     else:
#         MemoryRazdelsObj.name_id_rnv = []
#         if clicks_r6 != MemoryRazdelsObj.click_r6:
#             MemoryRazdelsObj.click_r6 = clicks_r6
#             return make_layout_razdels_rnv(objects_6=MemoryRazdelsObj.col_r6 + 1, objects_7=MemoryRazdelsObj.col_r7)
#         elif clicks_r7 != MemoryRazdelsObj.click_r7:
#             MemoryRazdelsObj.click_r7 = clicks_r7
#             return make_layout_razdels_rnv(objects_6=MemoryRazdelsObj.col_r6, objects_7=MemoryRazdelsObj.col_r7 + 1)


# Процедура чтоб перерисовать таблицу с новым разр
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
def make_rnv_table():
    df = ReadDBSQL.read_rnv_db()
    table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id='table_rnv',
                         style_data_conditional=style_data_conditional,
                         row_selectable='single',
                         # filter_action="native"
                         )
    return table

@app.callback(
    Output('rnv_null_save_div', 'children'),
    Input('save_new_rnv_to_db', 'n_clicks'),
    [State(key, 'value') for key in MemoryRazdelsObj.name_id_rnv],
    prevent_initial_call=True, )
def save_rnv(clicks, *args):
    if clicks is None:
        return ''
    else:


        new_dict_to_db = {}
        for idx, key in enumerate(MemoryRazdelsObj.name_id_rnv):
            new_key = str(key).replace('_', '.')
            new_dict_to_db[new_key] = args[idx]

        WriteRSNObj.add_rnv_to_sql(new_dict_to_db)

        return ''


@app.callback(
    Output('rnv_null_update_div', 'children'),
    Input('url', 'href'))
def display_page(href):
    if href is None:
        raise PreventUpdate

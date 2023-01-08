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

class MemoryRazdels:
    def __init__(self):
        self.col_r6 = 1
        self.col_r7 = 1

        self.click_r6 = 0
        self.click_r7 = 0

        self.name_id_rnv = []

MemoryRazdelsObj = MemoryRazdels()

WriteRSNObj = write_db.WriteDB()


def make_layout_new_rnv(objects_6=1, objects_7=1):
    rnv_div = []
    MemoryRazdelsObj.col_r6 = objects_6
    MemoryRazdelsObj.col_r7 = objects_7
    for idx, razdel in enumerate(vvod_text.rnv_razdels):
        # num_object = 1
        obj_max = 1
        if idx + 1 == 6:
            obj_max = objects_6
        if idx + 1 == 7:
            obj_max = objects_7
        for num_object in range(1, obj_max+1):
            tmp_razdel = []
            acc_tmp = []

            for label_x in vvod_text.rnv_labels:
                if str(label_x).startswith(str(idx + 1)):
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
                            label_x = label_x.replace('X', str(num_object))

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
                            razdel_text = razdel + f'-------- Объект №{num_object} --------'
                        acc_tmp = dbc.AccordionItem(tmp_razdel, title=razdel_text)
            rnv_div.append(acc_tmp)

    return rnv_div


layout = html.Div([
    html.H4('Новое разрешения на ввод', className="text-center", style={'margin': '10px'}),
    html.Div([
        html.Div([
            dbc.Button("Сохранить", color="success", className="me-1", id='save_new_rnv_to_db',
                       style={'margin': '10px'}, href="/rnv"),

            html.Div([
                dbc.Button("Добавить объект в раздел 6", color="warning", className="me-1",
                           id='button_rnv_add_obj_r6',
                           style={'margin': '10px'}),
                dbc.Button("Добавить объект в раздел 7", color="warning", className="me-1",
                           id='button_rnv_add_obj_r7',
                           style={'margin': '10px'}),
            ], style={'float': 'right'}),
        ]),
        dbc.Accordion(make_layout_new_rnv(), start_collapsed=True, id='rnv_razdels_accord'),
        html.Div(id='rnv_null_save_div')
    ])

])


@app.callback(
    Output('rnv_razdels_accord', 'children'),
    Input('button_rnv_add_obj_r6', 'n_clicks'),
    Input('button_rnv_add_obj_r7', 'n_clicks'),
    prevent_initial_call=True, )
def add_r6(clicks_r6, clicks_r7):
    if clicks_r6 is None:
        if clicks_r7 is None:
            return ''
    else:
        if clicks_r6 != MemoryRazdelsObj.click_r6:
            MemoryRazdelsObj.click_r6 = clicks_r6
            return make_layout_new_rnv(objects_6=MemoryRazdelsObj.col_r6 + 1, objects_7=MemoryRazdelsObj.col_r7)
        elif clicks_r7 != MemoryRazdelsObj.click_r7:
            MemoryRazdelsObj.click_r7 = clicks_r7
            return make_layout_new_rnv(objects_6=MemoryRazdelsObj.col_r6, objects_7=MemoryRazdelsObj.col_r7 + 1)


@app.callback(
    Output('rnv_null_save_div', 'children'),
    Input('save_new_rnv_to_db', 'n_clicks'),
    [State(key, 'value') for key in MemoryRazdelsObj.name_id_rnv],
    prevent_initial_call=True, )
def save_rnv(clicks, *args):
    if clicks is None:
        return ''
    else:
        MemoryRazdelsObj = MemoryRazdels()

        new_dict_to_db = {}
        for idx, key in enumerate(MemoryRazdelsObj.name_id_rnv):
            new_key = str(key).replace('_', '.')
            new_dict_to_db[new_key] = args[idx]

        WriteRSNObj.add_rnv_to_sql(new_dict_to_db)

        return ''
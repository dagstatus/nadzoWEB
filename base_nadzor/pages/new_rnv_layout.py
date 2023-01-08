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


def make_layout_new_rnv():
    rnv_div = []
    for idx, razdel in enumerate(vvod_text.rnv_razdels):
        tmp_razdel = []
        acc_tmp = []
        for label_x in vvod_text.rnv_labels:
            if str(label_x).startswith(str(idx + 1)):
                if label_x in vvod_text.rnv_non_input_labels:
                    tmp_razdel.append(dbc.Row(label_x, style={'font-weight': 'bold'}))
                else:

                    ############# temp ##############
                    if 'X' in label_x:
                        label_x = label_x.replace('X', '1')

                    tmp_razdel.append(
                        dbc.Row([
                            dbc.Label(label_x, width=10),
                            dbc.Col(dbc.Input(id=str(label_x.split()[0][:-1]).replace('.', '_'),
                                              ),
                                    width=10),
                        ], class_name="mb-3")
                    )

                    # print(str(label_x.split()[0][:-1]))
                    # print(self.edit_dict.get(str(label_x.split()[0][:-1]), ''))

                    acc_tmp = dbc.AccordionItem(tmp_razdel, title=razdel)
        rnv_div.append(acc_tmp)

    return rnv_div


layout = html.Div([
    html.H4('Новое разрешения на ввод', className="text-center", style={'margin': '10px'}),
    html.Div([
        dbc.Accordion(make_layout_new_rnv(), start_collapsed=True, ),
    ])

])

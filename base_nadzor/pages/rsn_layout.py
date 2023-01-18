import dash
import dash_auth
import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly
from base_nadzor.app import app
# from base_nadzor.read_db.read_db_func import ReadpandasRNV, SqlDB
from base_nadzor.pdf_rsn_creator import pdf_razr_stroit
from base_nadzor.pages import new_rnv_layout, razr_text
from base_nadzor.read_db import write_db

PdfClass = pdf_razr_stroit.CreatePdfClass()

ReadDBSQL = write_db.WriteDB()


def make_rsn_table():
    df = ReadDBSQL.read_rns_db()
    df = df.rename(columns=razr_text.rsn_labels_dict)
    table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id='table_rsn',
                                 style_data_conditional=style_data_conditional,
                                 row_selectable='single',
                                 style_header={'whiteSpace': 'normal', 'height': 'auto',
                                               'font_size': '10px',
                                               'text_align': 'center'
                                               },
                                 # style_data={'whiteSpace': 'normal', 'height': 'auto'},
                                 style_cell={'maxWidth': '400px', 'minWidth': '100px'},
                                 style_table={'overflowX': 'scroll'},

                                 # filter_action="native"
                                 )
    return table


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

layout = html.Div([
    html.H4('Разрешения на строительство', className="text-center", style={'margin': '10px'}),
    html.Div(children=[make_rsn_table()], id='rns_layout_table_update_div',
             style={'width': '100%',
                    # 'height': '75%',
                    # 'overflow': 'scroll',
                    'padding': '10px 10px 10px 20px'
                    }),
    # dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, id='table_rns'),

    html.Div(children=[
        dbc.Button("Добавить", color="success", className="me-1", id='add_rsn_btn', href="/new_rsn"),
        dbc.Button("Распечатать", color="success", className="me-1", id='print_rsn_btn'),
        dbc.Button("Изменить", color="success", className="me-1", id='edit_rsn_button', href='/rsn_editor'),
        dbc.Button("Загрузить из базы", color="warning", className="me-1", id='update_table_rsn_btn',
                   style={'float': 'center'}),
        dbc.Button("Удалить", color="danger", className="me-1", id='delete_rsn_btn', href="/rns",
                   style={'float': 'right'})
    ],
        style={'width': '100%', 'display': 'inline-block', 'margin': '20px'}),

    html.Div(id='null_div_rsn_editor'),
    html.Div(id='rsn_null_div_4_del'),

    html.Div(id='rnv_list_null', children=[
        dcc.Download(id="download_rsn_pdf"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Внесите данные и нажмите сохранить")),
                dbc.ModalBody(children=[
                    html.Div(id='rsn_list_null_new')
                ])

            ],
            id="modal-xl_rsn",
            size="xl",
            is_open=False,
        ),

    ]),
], className='container')


@app.callback(
    Output('rns_layout_table_update_div', 'children'),
    Input('update_table_rsn_btn', 'n_clicks'),
    # prevent_initial_call=True
)
def update_rsn_table(clicks):
    # if clicks is None:
    #     return ''
    # else:
    return make_rsn_table()


@app.callback(
    Output("table_rsn", "style_data_conditional"),
    [Input("table_rsn", "active_cell")]
)
def editor_rsn(active):
    style = style_data_conditional.copy()
    if active:
        style.append(
            {
                "if": {"row_index": active["row"]},
                "backgroundColor": "rgba(150, 180, 225, 0.2)",
                "border": "1px solid blue",
            }
        )
    return style

### EDIT LABEL
@app.callback(
    Output('null_div_rsn_editor', 'children'),
    Input('edit_rsn_button', 'n_clicks'),
    State('table_rsn', 'derived_virtual_data'),
    State('table_rsn', 'selected_rows'), prevent_initial_call=True, )
def open_rsn_editor(clicks, rows, id_row):
    if clicks is None:
        return ''
    else:
        import pickle
        data = {'id_row': id_row, 'row': rows[id_row[0]]}
        with open('rsn_editor.txt', 'wb') as f:
            pickle.dump(data, f)
            # print(data)
        return ''

# rnv_null_div_4_del
@app.callback(
    Output('rsn_null_div_4_del', 'children'),
    Input('delete_rsn_btn', 'n_clicks'),
    State('table_rsn', 'derived_virtual_data'),
    State('table_rsn', 'selected_rows'), prevent_initial_call=True, )
def opne_editor(clicks, rows, id_row):
    if clicks is None:
        return ''
    else:
        ReadDBSQL.del_rsn(rows[id_row[0]])
        return ''

@app.callback(
    Output('download_rsn_pdf', 'data'),
    Input('print_rsn_btn', 'n_clicks'),
    State('table_rsn', 'derived_virtual_data'),
    State('table_rsn', 'selected_rows'), prevent_initial_call=True, )
def printing_pdf(clicks, rows, id_row):
    if clicks is None:
        return ''
    else:
        PdfClass.input_data = rows[id_row[0]]
        filename_result = PdfClass.make_razr_pdf()
        PdfClass.input_data = rows[id_row[0]]
        return dcc.send_file(filename_result)
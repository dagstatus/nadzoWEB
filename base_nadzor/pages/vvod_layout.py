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
from base_nadzor.pages import new_rnv_layout
from base_nadzor.read_db import write_db

PdfClass = pdf_rnv_make_file.CreatePdfClass()

ReadDBSQL = write_db.WriteDB()


def make_rnv_table():
    df = ReadDBSQL.read_rnv_db()
    table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id='table_rnv',
                         style_data_conditional=style_data_conditional,
                         row_selectable='single',
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
    html.H4('Разрешения на ввод', className="text-center", style={'margin': '10px'}),
    html.Div(children=[make_rnv_table()], id='rnv_layout_table_update_div'),
    # dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, id='table_rns'),

    html.Div(children=[
        dbc.Button("Добавить", color="success", className="me-1", id='add_rnv_btn', href="/new_rnv"),
        dbc.Button("Распечатать", color="success", className="me-1", id='print_rnv_btn'),
        dbc.Button("Изменить", color="success", className="me-1", id='edit_rnv_button', href='/rnv_editor'),
        dbc.Button("Загрузить из базы", color="warning", className="me-1", id='update_table_rnv_btn', style={'float': 'center'}),
        dbc.Button("Удалить", color="danger", className="me-1", id='delete_rsn_btn', style={'float': 'right'})
    ], style={'width': '100%', 'display': 'inline-block', 'margin': '20px'}),

    html.Div(id='null_div_rnv_editor'),

    html.Div(id='rnv_list_null', children=[
        dcc.Download(id="download_rnv_pdf"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Внесите данные и нажмите сохранить")),
                dbc.ModalBody(children=[
                    html.Div(id='rsn_list_null_new')
                ])

            ],
            id="modal-xl_rnv",
            size="xl",
            is_open=False,
        ),

    ]),
], className='container')


@app.callback(
    Output('rnv_layout_table_update_div', 'children'),
    Input('update_table_rnv_btn', 'n_clicks'), prevent_initial_call=True)
def update_rnv_table(clicks):
    if clicks is None:
        return ''
    else:
        return make_rnv_table()



@app.callback(
    Output("table_rnv", "style_data_conditional"),
    [Input("table_rnv", "active_cell")]
)
def editor_rnv(active):
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
    Output('null_div_rnv_editor', 'children'),
    Input('edit_rnv_button', 'n_clicks'),
    State('table_rnv', 'derived_virtual_data'),
    State('table_rnv', 'selected_rows'), prevent_initial_call=True, )
def opne_editor(clicks, rows, id_row):
    if clicks is None:
        return ''
    else:
        import pickle
        data = {'id_row': id_row, 'row': rows[id_row[0]]}
        with open('rnv_editor.txt', 'wb') as f:
            pickle.dump(data, f)
            # print(data)
        return ''



@app.callback(
    Output('download_rnv_pdf', 'data'),
    Input('print_rnv_btn', 'n_clicks'),
    State('table_rnv', 'derived_virtual_data'),
    State('table_rnv', 'selected_rows'), prevent_initial_call=True, )
def printing_pdf(clicks, rows, id_row):
    if clicks is None:
        return ''
    else:
        PdfClass.input_data = rows[id_row[0]]
        filename_result = PdfClass.make_razr_pdf()
        PdfClass.input_data = rows[id_row[0]]
        return dcc.send_file(filename_result)


# @app.callback(
#     Output(Output('page-content', 'children'),
#            Input('add_rnv_btn', 'n_clicks')))
# def new_rsn(clicks):
#     if clicks is None:
#         return ''
#     else:
#         return new_rnv_layout.layout

import dash
import dash_auth
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly
from base_nadzor.app import app
from base_nadzor.read_db.read_db_func import ReadPandasRNS
from base_nadzor.pdf_rsn_creator import pdf_razr_stroit
from base_nadzor.pages import new_rsn_form

PdfClass = pdf_razr_stroit.CreatePdfClass()


ReadDBClass = ReadPandasRNS()
df = ReadDBClass.read_db()

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
    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id='table_rns',
                         style_data_conditional=style_data_conditional,
                         row_selectable='single',
                         # filter_action="native"
                         ),
    # dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, id='table_rns'),

    html.Div(children=[
        dbc.Button("Добавить", color="success", className="me-1", id='add_rsn_btn'),
        dbc.Button("Распечатать", color="success", className="me-1", id='print_rsn_btn'),
        dbc.Button("Удалить", color="danger", className="me-1", id='delete_rsn_btn', style={'float': 'right'})
    ], style={'width': '100%', 'display': 'inline-block', 'margin': '20px'}),
    html.Div(id='rsn_list_null', children=[
        dcc.Download(id="download_rsn_pdf"),
        dbc.Offcanvas(
            html.Div(id='rsn_list_null_new'),
            id="offcanvas_rsn",
            title="Добавление разрешения",
            backdrop='static',
            is_open=False,
            style={'width': '800px'}
        ),

    ]),
], className='container')


@app.callback(
    Output("table_rns", "style_data_conditional"),
    [Input("table_rns", "active_cell")]
)
def update_selected_row_color(active):
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

@app.callback(
    Output('download_rsn_pdf', 'data'),
    Input('print_rsn_btn', 'n_clicks'),
    State('table_rns', 'derived_virtual_data'),
    State('table_rns', 'selected_rows'), prevent_initial_call=True,)
def print(clicks, rows, id_row):
    if clicks is None:
        return ''
    else:

        PdfClass.input_data = rows[id_row[0]]
        filename_result = PdfClass.make_razr_pdf()
        PdfClass.input_data = rows[id_row[0]]
        return dcc.send_file(filename_result)


@app.callback(
    Output('rsn_list_null_new', 'children'), Output("offcanvas_rsn", "is_open"),
    Input('add_rsn_btn', 'n_clicks'), State("offcanvas_rsn", "is_open"),
    prevent_initial_call=True,)
def new_rsn(clicks, is_open_flag):
    if clicks is None:
        return '', is_open_flag
    else:
        return new_rsn_form.layout, not is_open_flag

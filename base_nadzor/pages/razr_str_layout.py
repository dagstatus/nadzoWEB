import dash
import dash_auth
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly
from base_nadzor.app import app
# from base_nadzor.read_db.read_db_func import ReadPandasRNS, SqlDB
from base_nadzor.pdf_rsn_creator import pdf_razr_stroit
# from base_nadzor.pages import new_rsn_form
from base_nadzor.read_db import write_db

PdfClass = pdf_razr_stroit.CreatePdfClass()

# ReadDBClass = ReadPandasRNS()
# df = ReadDBClass.read_db()

ReadDBSQL = write_db.WriteDB()
df = ReadDBSQL.read_rns_db()

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


def get_df_rns():
    df = ReadDBSQL.read_rns_db()
    return df

def make_rns_table():
    table = dash_table.DataTable(get_df_rns().to_dict('records'), [{"name": i, "id": i} for i in get_df_rns().columns],
                                 id='table_rns',
                                 style_data_conditional=style_data_conditional,
                                 row_selectable='single',
                                 # filter_action="native"
                                 )
    return table

def make_layout_rns():
    layout = html.Div([
        html.H4('Разрешения на строительство', className="text-center", style={'margin': '10px'}),
        # dash_table.DataTable(get_df_rns().to_dict('records'), [{"name": i, "id": i} for i in get_df_rns().columns],
        #                      id='table_rns',
        #                      style_data_conditional=style_data_conditional,
        #                      row_selectable='single',
        #                      # filter_action="native"
        #                      ),

        html.Div(
            children=[make_rns_table()],
            id='table_rns_div'
        )
        ,

        html.Div(children=[
            dbc.Button("Добавить", color="success", className="me-1", id='add_rsn_btn'),
            dbc.Button("Распечатать", color="success", className="me-1", id='print_rsn_btn'),
            dbc.Button("Изменить", color="success", className="me-1", id='edit_rsn_btn'),
            dbc.Button("Удалить", color="danger", className="me-1", id='delete_rsn_btn', style={'float': 'right'})
        ], style={'width': '100%', 'display': 'inline-block', 'margin': '20px'}),
        html.Div(id='rsn_list_null', children=[
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
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Внесите данные и нажмите сохранить")),
                    dbc.ModalBody(children=[
                        html.Div(id='rsn_list_null_edit')
                    ])

                ],
                id="modal-xl_rsn_edit",
                size="xl",
                is_open=False,
            ),

        ]),
    ], className='container')

    return layout


layout = make_layout_rns()


########################### NEW FORM ###########################
class NewRsnFormClass:
    def __init__(self, edit_flag=False, edit_dict={}):
        self.result = None
        self.razdels_tabs = ['Раздел 1. Реквизиты разрешения на строительство',
                             'Раздел 2. Информация о застройщике',
                             'Раздел 3. Информация об объекте капитального строительства',
                             'Раздел 4. Информация о земельном участке',
                             'Раздел 5. Сведения о проектной документации, типовом архитектурном решении',
                             'Раздел 6. Информация о результатах экспертизы проектной документации и государственной экологической экспертизы',
                             'Раздел 7. Проектные характеристики объекта капитального строительства',
                             'Раздел 8. Проектные характеристики линейного объекта']
        self.labels = [
            '1.1. Дата разрешения на строительство',
            '1.2. Номер разрешения на строительство',
            '1.3. Наименование органа (организации)',
            '1.4. Срок действия настоящего разрешения',
            '1.5. Дата внесения изменений или исправлений',
            '2.1. Сведения о физическом лице или индивидуальном предпринимателе',
            '2.1.1. Фамилия:',
            '2.1.2. Имя:',
            '2.1.3. Отчество',
            '2.1.4. ИНН:',
            '2.1.5. ОГРНИП',
            '2.2. Сведения о юридическом лице',
            '2.2.1. Полное наименование',
            '2.2.2. ИНН:',
            '2.2.3. ОГРН:',
            '3.1. Наименование объекта капитального строительства (этапа) в соответствии с проектной документацией:',
            '3.2. Вид выполняемых работ в отношении объекта капитального строительства в соответствии с проектной '
            'документацией',
            '3.3. Адрес (местоположение) объекта капитального строительства',
            '3.3.1. Субъект Российской Федерации:',
            '3.3.2. Муниципальный район, муниципальный округ, городской округ или внутригородская территория (для '
            'городов федерального значения) в составе субъекта Российской Федерации, федеральная территория:',
            '3.3.3. Городское или сельское поселение в составе муниципального района (для муниципального района) или '
            'внутригородского района городского округа (за исключением зданий, строений, сооружений, расположенных на '
            'федеральных территориях):',
            '3.3.4. Тип и наименование населенного пункта:',
            '3.3.5. Наименование элемента планировочной структуры:',
            '3.3.6. Наименование элемента улично-дорожной сети:',
            '3.3.7. Тип и номер здания (сооружения):',
            '4.1. Кадастровый номер земельного участка (земельных участков), в границах которого (которых) расположен '
            'или планируется расположение объекта капитального строительства',
            '4.2. Площадь земельного участка (земельных участков), в границах которого (которых) расположен или '
            'планируется расположение объекта капитального строительства',
            '4.3. Сведения о градостроительном плане земельного участка',
            '4.3.X.1. Дата:',
            '4.3.X.2. Номер:',
            '4.3.X.3. Наименование органа, выдавшего градостроительный план земельного участка:',
            '4.4. Условный номер земельного участка (земельных участков) на утвержденной схеме расположения '
            'земельного участка или земельных участков на кадастровом плане территории (при необходимости)',
            '4.5. Сведения о схеме расположения земельного участка или земельных участков на кадастровом плане '
            'территории',
            '4.5.1. Дата решения:',
            '4.5.2. Номер решения:',
            '4.5.3. Наименовании организации, уполномоченного органа или лица, принявшего решение об утверждении '
            'схемы расположения земельного участка или земельных участков:',
            '4.6. Информация о документации по планировке территории',
            '4.6.1. Сведения о проекте планировки территории',
            '4.6.1.X.1. Дата решения:',
            '4.6.1.X.2. Номер решения:',
            '4.6.1.X.3. Наименование организации, уполномоченного органа или лица, принявшего решение об утверждении '
            'проекта планировки территории:',
            '4.6.2. Сведения о проекте межевания территории',
            '4.6.2.X.1. Дата решения:',
            '4.6.2.X.2. Номер решения:',
            '4.6.2.X.3. Наименовании организации, уполномоченного органа или лица, принявшего решение об утверждении '
            'проекта межевания территории:',
            '5.1. Сведения о разработчике - индивидуальном предпринимателе',
            '5.1.1. Фамилия:',
            '5.1.2. Имя:',
            '5.1.3. Отчество',
            '5.1.4. ИНН:',
            '5.1.5. ОГРНИП:',
            '5.2. Сведения о разработчике - юридическом лице',
            '5.2.1. Полное наименование',
            '5.2.2. ИНН:',
            '5.2.3. ОГРН:',
            '5.3. Дата утверждения (при наличии)',
            '5.4. Номер (при наличии)',
            '5.5. Типовое архитектурное решение объекта капитального строительства, утвержденное для исторического '
            'поселения (при наличии)',
            '5.5.1. Дата:',
            '5.5.2. Номер:',
            '5.5.3. Наименование документа:',
            '5.5.4. Наименование уполномоченного органа, принявшего решение об утверждении типового архитектурного '
            'решения:',
            '6.1. Сведения об экспертизе проектной документации',
            '6.1.X.1. Дата утверждения:',
            '6.1.X.2. Номер:',
            '6.1.X.3. Наименование органа или организации, 3выдавшей положительное заключение экспертизы проектной '
            'документации:',
            '6.2. Сведения о государственной экологической экспертизе',
            '6.2.X.1. Дата утверждения:',
            '6.2.X.2. Номер:',
            '6.2.X.3. Наименование органа, утвердившего положительное заключение государственной экологической '
            'экспертизы:',
            '6.3. Подтверждение соответствия вносимых в проектную документацию изменений требованиям, указанным '
            'в части 3.8 статьи 49 Градостроительного кодекса Российской Федерации',
            '6.3.1. Дата:',
            '6.3.2. Номер:',
            '6.3.3. Сведения о лице, утвердившем указанное подтверждение',
            '6.4. Подтверждение соответствия вносимых в проектную документацию изменений требованиям, указанным '
            'в части 3.9 статьи 49 Градостроительного кодекса Российской Федерации',
            '6.4.1. Дата:',
            '6.4.2. Номер:',
            '6.4.3. Наименование органа исполнительной власти или организации, проводившей оценку соответствия:',
            '7.X. Наименование объекта капитального строительства, предусмотренного проектной документацией',
            '7.X.1. Вид объекта капитального строительства',
            '7.X.2. Назначение объекта',
            '7.X.3. Кадастровый номер реконструируемого объекта капитального строительства',
            '7.X.4. Площадь застройки (кв.м)',
            '7.X.4.1. Площадь застройки части объекта капитального строительства (кв.м)',
            '7.X.5. Площадь (кв.м)',
            '7.X.5.1. Площадь части объекта капитального строительства (кв.м)',
            '7.X.6. Площадь нежилых помещений (кв.м):',
            '7.X.7. Площадь жилых помещений (кв.м):',
            '7.X.8. Количество помещений (штук):',
            '7.X.9. Количество нежилых помещений (штук):',
            '7.X.10. Количество жилых помещений (штук):',
            '7.X.11. в том числе квартир (штук):',
            '7.X.12. Количество машино-мест (штук):',
            '7.X.13. Количество этажей:',
            '7.X.14. в том числе, количество подземных этажей:',
            '7.X.15. Вместимость (человек):',
            '7.X.16. Высота (м):',
            '7.X.17. Иные показатели',
            '8.X. Наименование линейного объекта, предусмотренного проектной документацией',
            '8.X.1. Кадастровый номер реконструируемого линейного объекта:',
            '8.X.2. Протяженность (м)',
            '8.X.2.1. Протяженность участка или части линейного объекта (м)',
            '8.X.3. Категория (класс):',
            '8.X.4. Мощность (пропускная способность, грузооборот, интенсивность движения):',
            '8.X.5. Тип (кабельная линия электропередачи, воздушная линия электропередачи, кабельно-воздушная линия '
            'электропередачи), уровень напряжения линий электропередачи:',
            '8.X.6. Иные показатели',
        ]

        self.non_input_labels = [
            '2.1. Сведения о физическом лице или индивидуальном предпринимателе',
            '2.2. Сведения о юридическом лице',
            '3.3. Адрес (местоположение) объекта капитального строительства',
            '4.3. Сведения о градостроительном плане земельного участка',
            '4.5. Сведения о схеме расположения земельного участка или земельных участков на кадастровом плане '
            'территории',
            '4.6. Информация о документации по планировке территории',
            '4.6.1. Сведения о проекте планировки территории',
            '4.6.2. Сведения о проекте межевания территории',
            '5.1. Сведения о разработчике - индивидуальном предпринимателе',
            '5.2. Сведения о разработчике - юридическом лице',
            '5.5. Типовое архитектурное решение объекта капитального строительства, утвержденное для исторического '
            'поселения (при наличии)',
            '6.1. Сведения об экспертизе проектной документации',
            '6.2. Сведения о государственной экологической экспертизе',
            '6.3. Подтверждение соответствия вносимых в проектную документацию изменений требованиям, указанным '
            'в части 3.8 статьи 49 Градостроительного кодекса Российской Федерации',
            '6.4. Подтверждение соответствия вносимых в проектную документацию изменений требованиям, указанным '
            'в части 3.9 статьи 49 Градостроительного кодекса Российской Федерации'
        ]

        self.state_inputs = []

        self.edit_flag = edit_flag

        self.edit_dict = edit_dict

    def make_rsn_new_form(self):
        big_form = []
        for idx, razdel in enumerate(self.razdels_tabs):
            tmp_razdel = []
            acc_tmp = []
            for label_x in self.labels:
                if str(label_x).startswith(str(idx + 1)):
                    if label_x in self.non_input_labels:
                        tmp_razdel.append(dbc.Row(label_x, style={'font-weight': 'bold'}))
                    else:

                        ############# temp ##############
                        if 'X' in label_x:
                            label_x = label_x.replace('X', '1')

                        tmp_razdel.append(
                            dbc.Row([
                                dbc.Label(label_x, width=10),
                                dbc.Col(dbc.Input(id=str(label_x.split()[0][:-1]).replace('.', '_'),
                                                  value=self.edit_dict.get(
                                                      str(label_x.split()[0][:-1]), ''
                                                  )),
                                        width=10),
                            ], class_name="mb-3")
                        )

                        # print(str(label_x.split()[0][:-1]))
                        # print(self.edit_dict.get(str(label_x.split()[0][:-1]), ''))

                        self.state_inputs.append(str(label_x.split()[0][:-1]).replace('.', '_'))
                        acc_tmp = dbc.AccordionItem(tmp_razdel, title=razdel)
            big_form.append(acc_tmp)

        return big_form


NewRsnObj = NewRsnFormClass(edit_flag=False, edit_dict={})
WriteRSNObj = write_db.WriteDB()

layout_new_rsn = html.Div(children=[
    dbc.Accordion(NewRsnObj.make_rsn_new_form(), start_collapsed=True, ),
    dbc.Button("Сохранить", color="success", className="me-1", id='save_new_rsn_to_db', style={'margin': '10px'}),
    html.Div(id='new_rsn_result_null')
])


# def edit_layout_func(edit_flag=False, edit_dict={}):
#     EditRsnObj = NewRsnFormClass(edit_flag=edit_flag, edit_dict=edit_dict)
#     layout_edit = html.Div(children=[
#         dbc.Accordion(EditRsnObj.make_rsn_new_form(), start_collapsed=True,),
#         dbc.Button("Сохранить", color="success", className="me-1", id='save_new_rsn_to_db', style={'margin': '10px'}),
#         html.Div(id='new_rsn_result_null')
#     ])
#     return layout_edit


@app.callback(
    Output('new_rsn_result_null', 'children'),
    Output('table_rns', 'data'),
    Input('save_new_rsn_to_db', 'n_clicks'),
    [State(key, 'value') for key in NewRsnObj.state_inputs],
    prevent_initial_call=True, )
def save_rsn(clicks, *args):
    if clicks is None:
        return '', ''
    else:
        new_dict_to_db = {}
        for idx, key in enumerate(NewRsnObj.state_inputs):
            new_key = str(key).replace('_', '.')
            new_dict_to_db[new_key] = args[idx]

        if NewRsnObj.edit_flag:
            WriteRSNObj.edit_rns_sql(dict_new=new_dict_to_db,
                                     uid_father=NewRsnObj.edit_dict.get('uid'),
                                     version=NewRsnObj.edit_dict.get('version'))
            NewRsnObj.edit_flag = False
        else:
            WriteRSNObj.add_rsn_to_sql(new_dict_to_db)

        data_to_table = get_df_rns().to_dict('records')
        return '', data_to_table


########################### NEW FORM ###########################


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
    State('table_rns', 'selected_rows'), prevent_initial_call=True, )
def print(clicks, rows, id_row):
    if clicks is None:
        return ''
    else:

        PdfClass.input_data = rows[id_row[0]]
        filename_result = PdfClass.make_razr_pdf()
        PdfClass.input_data = rows[id_row[0]]
        return dcc.send_file(filename_result)


@app.callback(
    Output('rsn_list_null_edit', 'children'), Output('modal-xl_rsn_edit', 'is_open'),
    Input('edit_rsn_btn', 'n_clicks'),
    State('table_rns', 'derived_virtual_data'),
    State('table_rns', 'selected_rows'), prevent_initial_call=True, )
def edit(clicks, rows, id_row):
    if clicks is None:
        return '', False
    else:
        # NewRsnObj = NewRsnFormClass(edit_flag=False, edit_dict={})
        # WriteRSNObj = write_db.WriteDB()
        # new_rsn_form.NewRsnObj = new_rsn_form.NewRsnFormClass(edit_flag=True, edit_dict=rows[id_row[0]])
        # edit_dict = df.loc[id_row[0]].to_dict()
        NewRsnObj.edit_dict = df.loc[id_row[0]].to_dict()
        NewRsnObj.edit_flag = True

        layout_edit_rsn = html.Div(children=[
            dbc.Accordion(NewRsnObj.make_rsn_new_form(), start_collapsed=True, ),
            dbc.Button("Сохранить", color="success", className="me-1", id='save_new_rsn_to_db',
                       style={'margin': '10px'}),
            html.Div(id='new_rsn_result_null')
        ])

        return layout_edit_rsn, True


##### DELETE
@app.callback(
    Output('table_rns_div', 'children'),
    Input('delete_rsn_btn', 'n_clicks'),
    State('table_rns', 'derived_virtual_data'),
    State('table_rns', 'selected_rows'), prevent_initial_call=True, )
def edit(clicks, rows, id_row):
    if clicks is None:
        return ''
    else:
        WriteRSNObj.del_rsn(rows[id_row[0]])
        return make_rns_table()







@app.callback(
    Output('rsn_list_null_new', 'children'), Output('modal-xl_rsn', 'is_open'),
    Input('add_rsn_btn', 'n_clicks'),
    prevent_initial_call=True, )
def new_rsn(clicks):
    if clicks is None:
        return '', False
    else:
        return layout_new_rsn, True

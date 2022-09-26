from fpdf import FPDF
from base_nadzor.settings_nadzor import settings

SettingsClass = settings.SettingsNadzor()
# НАДО ПЕРЕНЕСТИ В КОНФИГ
# owner_adrr = '          367000, РД, г.Махачкала, ул. Коркмасова, 18                 e-mail: uaig.mah@mail.ru'
# tel_number_owner = 'тел. (8722) 78-02-72          '

owner_adrr = SettingsClass.settings_dict.get('nadzor_adres')
owner_email = SettingsClass.settings_dict.get('nadzor_email')
owner_tel = SettingsClass.settings_dict.get('nadzor_tel')
ownner_name = SettingsClass.settings_dict.get('nadzor_name')
owner_doljnost = SettingsClass.settings_dict.get('nadzor_doljnost')
owner_podpis_fio = SettingsClass.settings_dict.get('nadzor_fio')


class PDF(FPDF):
    def header(self):
        if self.page_no() != 1:
            self.set_font('PTSerif', '', 10)
            self.cell(w=0, h=10.0, align='R', txt=f'стр. {self.page_no()}')
            self.ln(10)
      # nothing happens when it is executed.


class CreatePdfClass:
    def __init__(self):
        self.pdf = PDF(orientation='P', unit='mm', format='A4')  # pdf object
        self.pdf.add_page()
        self.input_data = None

    def make_razr_pdf(self):
        print(self.input_data)
        INPUT_DATA = self.input_data

        # INPUT_DATA = {'1.1': '06.09.2022г.', '1.2': '05-308-027-2022', '1.3': 'Управление архитектуры и градостроительства Администрации города Махачкалы', '1.4': '06.09.2024г.', '2.1.1': 'Пирмагомедов', '2.1.2': 'Разим', '2.1.3': 'Алифендиевич', '2.1.4': '056006731592', '3.1': '4-х этажное торговое здание', '3.2': 'строительство', '3.3.1': 'Республика Дагестан\r', '3.3.2': 'ГОсВД «город Махачкала»', '3.3.6': 'пр-кт Гамидова', '3.3.7': 'уч.3, 3б\n', '4.1': '05:40:000060:14693', '4.2': '237 кв.м.', '4.3.1.1': '22.10.2021г.', '4.3.1.2': 'РФ-05-2-01-1-00-2021-3417', '4.3.1.3': 'Управление архитектуры и градостроительства Администрации города Махачкалы', '5.2.1': 'ООО ПЦ «Инвест-Проект»', '5.2.2': '0571036001', '5.2.3': '1140571001064', '6.1.1.1': '05.09.2022г.', '6.1.1.2': '05-2-1-3-063780-2022', '6.1.1.3': 'ООО «Коин-С»', '7.1': '4-х этажное торговое здание', '7.1.1': 'здание', '7.1.2': 'нежилое', '7.1.3': '184.5', '7.1.4': '657.97', '7.1.13': '4', '7.1.16': '15.95'}

        self.pdf.set_xy(x=93, y=15)
        self.pdf.image('base_nadzor/pdf_rsn_creator/gerb.jpg', link='', type='', w=25, h=19)


        # Document title centered, 'B'old, 14 pt
        self.pdf.add_font('PTSerif', '', 'base_nadzor/pdf_rsn_creator/fonts/PTSerif-Regular.ttf', uni=True)
        self.pdf.add_font('PTSerifBold', '', 'base_nadzor/pdf_rsn_creator/fonts/PTSerif-Bold.ttf', uni=True)


        self.pdf.set_font('PTSerif', '', 15)

        start_head_text = 20

        self.pdf.set_xy(0.0, start_head_text)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(w=210.0, h=40.0, align='C', txt="АДМИНИСТРАЦИЯ ГОРОДСКОГО ОКРУГА", border=0)
        self.pdf.set_xy(0.0, start_head_text + 7)

        self.pdf.cell(w=210.0, h=40.0, align='C', txt='С ВНУТРИГОРОДСКИМ ДЕЛЕНИЕМ «ГОРОД МАХАЧКАЛА»', border=0)


        self.pdf.set_xy(0.0, start_head_text + 17)
        self.pdf.set_font('PTSerifBold', '', 18)
        self.pdf.cell(w=210.0, h=40.0, align='C', txt=ownner_name, border=0)
        self.pdf.set_font('PTSerif', '', 15)
        # pdf.set_xy(0.0, start_head_text + 25)
        # pdf.cell(w=210.0, h=40.0, align='C', txt='КАПИТАЛЬНОГО СТРОИТЕЛЬСТВА')

        epw = self.pdf.w - 2 * self.pdf.l_margin
        w_1_from_5 = (epw / 5)
        w_3_from_5 = (epw / 5) * 3

        self.pdf.set_xy(self.pdf.l_margin, start_head_text + 28)
        self.pdf.set_font('PTSerif', '', 10)
        self.pdf.cell(w=w_3_from_5, h=40.0, align='L', txt=owner_adrr)
        self.pdf.cell(w=w_1_from_5, h=40.0, align='R', txt=owner_email)
        self.pdf.cell(w=w_1_from_5, h=40.0, align='R', txt=owner_tel)

        self.pdf.set_line_width(0.5)
        self.pdf.line(10, start_head_text + 51, 200, start_head_text + 51)
        self.pdf.set_line_width(0.0)
        self.pdf.line(10, start_head_text + 52, 200, start_head_text + 52)


        self.pdf.set_font('PTSerif', '', 8)
        self.pdf.set_xy(x=120, y=start_head_text + 55)
        w_pril = 210 - self.pdf.r_margin - 120
        self.pdf.multi_cell(w=w_pril, h=4, align='R', border=0,
                            txt='Приложение N 1 к приказу Министерства строительства и жилищно-коммунального хозяйства Российской Федерации от 3 июня 2022 года N 446/пр')

        self.pdf.set_xy(0.0, start_head_text + 62.5)
        self.pdf.set_font('PTSerifBold', '', 16)
        self.pdf.cell(w=210.0, h=40.0, align='C', txt='РАЗРЕШЕНИЕ НА СТРОИТЕЛЬСТВО')

        self.pdf.set_xy(0.0, start_head_text + 67.5)
        self.pdf.set_font('PTSerif', '', 10)
        self.pdf.cell(w=200.0, h=40.0, align='R', txt=f'стр. {self.pdf.page_no()}')

        self.pdf.set_xy(0.0, start_head_text + 93.5)

        data_table = [
            ['Раздел 1. Реквизиты разрешения на строительство'],
            ['1.1. Дата разрешения на строительство :', INPUT_DATA.get('1.1')],
            ['1.2. Номер разрешения на строительство :', INPUT_DATA.get('1.2')],
            ['1.3. Наименование органа (организации) :', INPUT_DATA.get('1.3')],
            ['1.4. Срок действия настоящего разрешения :', INPUT_DATA.get('1.4')],
            ['1.5. Дата внесения изменений или исправлений :', INPUT_DATA.get('1.5')],
            ['Раздел 2. Информация о застройщике'],
            ['2.1. Сведения о физическом лице или индивидуальном предпринимателе'],
            ['2.1.1. Фамилия:', INPUT_DATA.get('2.1.1')],
            ['2.1.2. Имя:', INPUT_DATA.get('2.1.2')],
            ['2.1.3. Отчество :', INPUT_DATA.get('2.1.3')],
            ['2.1.4. ИНН:', INPUT_DATA.get('2.1.4')],
            ['2.1.5. ОГРНИП :', INPUT_DATA.get('2.1.5')],
            ['2.2. Сведения о юридическом лице'],
            ['2.2.1. Полное наименование :', INPUT_DATA.get('2.2.1')],
            ['2.2.2. ИНН:', INPUT_DATA.get('2.2.2')],
            ['2.2.3. ОГРН:', INPUT_DATA.get('2.2.3')],
            ['Раздел 3. Информация об объекте капитального строительства'],
            ['3.1. Наименование объекта капитального строительства (этапа) в соответствии с проектной документацией:'
                , INPUT_DATA.get('3.1')],
            ['3.2. Вид выполняемых работ в отношении объекта капитального строительства в соответствии с проектной '
             'документацией :',
             INPUT_DATA.get('3.2')],
            ['3.3. Адрес (местоположение) объекта капитального строительства'],
            ['3.3.1. Субъект Российской Федерации:', INPUT_DATA.get('3.3.1')],
            ['3.3.2. Муниципальный район, муниципальный округ, городской округ или внутригородская территория (для '
             'городов федерального значения) в составе субъекта Российской Федерации, федеральная территория:',
             INPUT_DATA.get('3.3.2')],
            ['3.3.3. Городское или сельское поселение в составе муниципального района (для муниципального района) '
             'или внутригородского района городского округа (за исключением зданий, строений, сооружений, '
             'расположенных на федеральных территориях):', INPUT_DATA.get('3.3.3')],
            ['3.3.4. Тип и наименование населенного пункта:', INPUT_DATA.get('3.3.4')],
            ['3.3.5. Наименование элемента планировочной структуры:', INPUT_DATA.get('3.3.5')],
            ['3.3.6. Наименование элемента улично-дорожной сети:', INPUT_DATA.get('3.3.6')],
            ['3.3.7. Тип и номер здания (сооружения):', INPUT_DATA.get('3.3.7')],
            ['Раздел 4. Информация о земельном участке'],
            [
                '4.1. Кадастровый номер земельного участка (земельных участков), в границах которого (которых) '
                'расположен или планируется расположение объекта капитального строительства',
                INPUT_DATA.get("4.1")],
            [
                '4.2. Площадь земельного участка (земельных участков), в границах которого (которых) расположен или '
                'планируется расположение объекта капитального строительства', INPUT_DATA.get("4.2")],
            ['4.3. Сведения о градостроительном плане земельного участка'],
            ['4.3.1.1. Дата:', INPUT_DATA.get("4.3.1.1")],
            ['4.3.1.2. Номер:', INPUT_DATA.get("4.3.1.2")],
            ['4.3.1.3. Наименование органа, выдавшего градостроительный план земельного участка:',
                INPUT_DATA.get("4.3.1.3")],
            [
                '4.4. Условный номер земельного участка (земельных участков) на утвержденной схеме расположения '
                'земельного участка или земельных участков на кадастровом плане территории (при необходимости)',
                INPUT_DATA.get("4.4")],
            [
                '4.5. Сведения о схеме расположения земельного участка или земельных участков на кадастровом плане '
                'территории'],
            ['4.5.1. Дата решения:', INPUT_DATA.get("4.5.1")],
            ['4.5.2. Номер решения:', INPUT_DATA.get("4.5.2")],
            [
                '4.5.3. Наименовании организации, уполномоченного органа или лица, принявшего решение об утверждении '
                'схемы расположения земельного участка или земельных участков:', INPUT_DATA.get("4.5.3")],
            ['4.6. Информация о документации по планировке территории'],
            ['4.6.1. Сведения о проекте планировки территории'],
            ['4.6.1.X.1. Дата решения:', INPUT_DATA.get("4.6.1.X.1")],
            ['4.6.1.1.2. Номер решения:', INPUT_DATA.get("4.6.1.1.2")],
            [
                '4.6.1.1.3. Наименование организации, уполномоченного органа или лица, принявшего решение об '
                'утверждении проекта планировки территории:', INPUT_DATA.get("4.6.1.1.3")],
            ['4.6.2. Сведения о проекте межевания территории'],
            ['4.6.2.1.1. Дата решения:', INPUT_DATA.get("4.6.2.1.1")],
            ['4.6.2.1.2. Номер решения:', INPUT_DATA.get("4.6.2.1.2")],
            [
                '4.6.2.1.3. Наименовании организации, уполномоченного органа или лица, принявшего решение об '
                'утверждении проекта межевания территории:', INPUT_DATA.get("4.6.2.1.3")],
            ['Раздел 5. Сведения о проектной документации, типовом архитектурном решении'],
            ['5.1. Сведения о разработчике - индивидуальном предпринимателе'],
            ['5.1.1. Фамилия:', INPUT_DATA.get("5.1.1")],
            ['5.1.2. Имя:', INPUT_DATA.get("5.1.2")],
            ['5.1.3. Отчество', INPUT_DATA.get("5.1.3")],
            ['5.1.4. ИНН:', INPUT_DATA.get("5.1.4")],
            ['5.1.5. ОГРНИП:', INPUT_DATA.get("5.1.5")],
            ['5.2. Сведения о разработчике - юридическом лице'],
            ['5.2.1. Полное наименование', INPUT_DATA.get("5.2.1")],
            ['5.2.2. ИНН:', INPUT_DATA.get("5.2.2")],
            ['5.2.3. ОГРН:', INPUT_DATA.get("5.2.3")],
            ['5.3. Дата утверждения (при наличии)', INPUT_DATA.get("5.3")],
            ['5.4. Номер (при наличии)', INPUT_DATA.get("5.4")],
            [
                '5.5. Типовое архитектурное решение объекта капитального строительства, утвержденное для '
                'исторического поселения (при наличии)'],
            ['5.5.1. Дата:', INPUT_DATA.get("5.5.1")],
            ['5.5.2. Номер:', INPUT_DATA.get("5.5.2")],
            ['5.5.3. Наименование документа:', INPUT_DATA.get("5.5.3")],
            [
                '5.5.4. Наименование уполномоченного органа, принявшего решение об утверждении типового '
                'архитектурного решения:', INPUT_DATA.get("5.5.4")],
            ['Раздел 6. Информация о результатах экспертизы проектной документации и государственной экологической экспертизы'],
            ['6.1. Сведения об экспертизе проектной документации'],
            ['6.1.1.1. Дата утверждения:', INPUT_DATA.get("6.1.1.1")],
            ['6.1.1.2. Номер:', INPUT_DATA.get("6.1.1.2")],
            [
                '6.1.1.3. Наименование органа или организации, выдавшей положительное заключение экспертизы '
                'проектной документации:', INPUT_DATA.get("6.1.1.3")],
            ['6.2. Сведения о государственной экологической экспертизе'],
            ['6.2.1.1. Дата утверждения:', INPUT_DATA.get("6.2.1.1")],
            ['6.2.1.2. Номер:', INPUT_DATA.get("6.2.1.2")],
            [
                '6.2.1.3. Наименование органа, утвердившего положительное заключение государственной экологической '
                'экспертизы:', INPUT_DATA.get("6.2.1.3")],
            [
                '6.3. Подтверждение соответствия вносимых в проектную документацию изменений требованиям, указанным в '
                'части 3.8 статьи 49 Градостроительного кодекса Российской Федерации'],
            ['6.3.1. Дата:', INPUT_DATA.get("6.3.1")],
            ['6.3.2. Номер:', INPUT_DATA.get("6.3.2")],
            ['6.3.3. Сведения о лице, утвердившем указанное подтверждение', INPUT_DATA.get("6.3.3")],
            [
                '6.4. Подтверждение соответствия вносимых в проектную документацию изменений требованиям, указанным в '
                'части 3.9 статьи 49 Градостроительного кодекса Российской Федерации'],
            ['6.4.1. Дата:', INPUT_DATA.get("6.4.1")],
            ['6.4.2. Номер:', INPUT_DATA.get("6.4.2")],
            [
                '6.4.3. Наименование органа исполнительной власти или организации, проводившей оценку соответствия:',
                INPUT_DATA.get("6.4.3")],
            ['Раздел 7. Проектные характеристики объекта капитального строительства'],
            [
                '7.1. Наименование объекта капитального строительства, предусмотренного проектной документацией',
                INPUT_DATA.get("7.1")],
            ['7.1.1. Вид объекта капитального строительства', INPUT_DATA.get("7.1.1")],
            ['7.1.2. Назначение объекта', INPUT_DATA.get("7.1.2")],
            ['7.1.3. Кадастровый номер реконструируемого объекта капитального строительства', INPUT_DATA.get("7.1.3")],
            ['7.1.4. Площадь застройки (кв.м)', INPUT_DATA.get("7.1.4")],
            ['7.1.4.1. Площадь застройки части объекта капитального строительства (кв.м)', INPUT_DATA.get("7.1.4.1")],
            ['7.1.5. Площадь (кв.м)', INPUT_DATA.get("7.1.5")],
            ['7.1.5.1. Площадь части объекта капитального строительства (кв.м)', INPUT_DATA.get("7.1.5.1")],
            ['7.1.6. Площадь нежилых помещений (кв.м):', INPUT_DATA.get("7.1.6")],
            ['7.1.7. Площадь жилых помещений (кв.м):', INPUT_DATA.get("7.1.7")],
            ['7.1.8. Количество помещений (штук):', INPUT_DATA.get("7.1.8")],
            ['7.1.9. Количество нежилых помещений (штук):', INPUT_DATA.get("7.1.9")],
            ['7.1.10. Количество жилых помещений (штук):', INPUT_DATA.get("7.1.10")],
            ['7.1.11. в том числе квартир (штук):', INPUT_DATA.get("7.1.11")],
            ['7.1.12. Количество машино-мест (штук):', INPUT_DATA.get("7.1.12")],
            ['7.1.13. Количество этажей:', INPUT_DATA.get("7.1.13")],
            ['7.1.14. в том числе, количество подземных этажей:', INPUT_DATA.get("7.1.14")],
            ['7.1.15. Вместимость (человек):', INPUT_DATA.get("7.1.15")],
            ['7.1.16. Высота (м):', INPUT_DATA.get("7.1.16")],
            ['7.1.17. Иные показатели', INPUT_DATA.get("7.1.17")],
            ['Раздел 8. Проектные характеристики линейного объекта'],
            ['8.1. Наименование линейного объекта, предусмотренного проектной документацией', INPUT_DATA.get("8.Х")],
            ['8.1.1. Кадастровый номер реконструируемого линейного объекта:', INPUT_DATA.get("8.1.1")],
            ['8.1.2. Протяженность (м)', INPUT_DATA.get("8.1.2")],
            ['8.1.2.1. Протяженность участка или части линейного объекта (м)', INPUT_DATA.get("8.1.2.1")],
            ['8.1.3. Категория (класс):', INPUT_DATA.get("8.1.3")],
            [
                '8.1.4. Мощность (пропускная способность, грузооборот, интенсивность движения):',
                INPUT_DATA.get("8.1.4")],
            [
                '8.1.5. Тип (кабельная линия электропередачи, воздушная линия электропередачи, кабельно-воздушная '
                'линия электропередачи), уровень напряжения линий электропередачи:', INPUT_DATA.get("8.1.5")],
            ['8.1.6. Иные показатели', INPUT_DATA.get("8.1.6")],

        ]

        # Метод смотрит каких разделов нету во вводе
        def make_no_need_razdels(input_data: dict):
            res = []
            need_razdels = [1, 2, 3, 4, 5, 6, 7, 8]
            include_razdels = []
            for key, value in input_data.items():
                if str(key[0])[0].isdigit():
                    if int(str(key[0])) in need_razdels:
                        if value is not None:
                            include_razdels.append(int(str(key[0])))

            for _r in need_razdels:
                if _r in include_razdels:
                    continue
                else:
                    res.append(_r)
            return res

        not_need_radels_list = make_no_need_razdels(INPUT_DATA)


        def check_cell_h(text_cell):
            pdf_test = PDF(orientation='P', unit='mm', format='A4')  # pdf object
            pdf_test.add_page()
            pdf_test.add_font('PTSerif', '', 'base_nadzor/pdf_rsn_creator/fonts/PTSerif-Regular.ttf', uni=True)
            pdf_test.set_font('PTSerif', '', 10)
            th_test = pdf_test.font_size
            cell_h_test = 1.5 * th_test
            top_test = pdf_test.y
            epw_test = pdf_test.w - 2 * pdf_test.l_margin
            test_cell_w = epw_test / 2
            pdf_test.multi_cell(test_cell_w, cell_h_test, str(text_cell), border=1)
            multicell_test_h = pdf_test.get_y() - top_test
            # pdf_test.output('test2.pdf', 'F')
            return multicell_test_h


        # Effective page width, or just epw
        epw = self.pdf.w - 2 * self.pdf.l_margin
        th = self.pdf.font_size
        cell_h = 1.4 * th
        multicell_h = cell_h

        monocolumns = ('2.1', '2.2', '3.3', '4.3', '4.5', '4.6', '5.1', '5.2', '5.5','6.1', '6.2', '6.3', '6.4')
        self.pdf.b_margin = self.pdf.b_margin - 10
        self.pdf.ln(0.5)
        for idx_row, row in enumerate(data_table):
            self.pdf.set_font('PTSerif', '', 10)
            align_one_colun = 'L'
            if len(row) < 2:

                # Надо проверить следующая строка влазит на страницу или нет
                check_y = self.pdf.y
                ostatok_y = self.pdf.h - self.pdf.t_margin - self.pdf.b_margin - check_y
                flag_new_page = False
                for _datum in data_table[idx_row + 1]:
                    if check_cell_h(_datum) > ostatok_y:
                        flag_new_page = True
                if flag_new_page:
                    self.pdf.add_page()

                if str(row[0]).startswith('Раздел'):
                    self.pdf.set_font('PTSerifBold', '', 12)
                    align_one_colun = 'C'

                    # TEMP !!!!!!#############
                    # if str(row[0]).startswith('Раздел 4'):
                    #     self.pdf.add_page()

                    flag_not_need_razdel = False
                    for _razdel_del in not_need_radels_list:
                        if str(row[0]).startswith(f'Раздел {_razdel_del}'):
                            flag_not_need_razdel = True

                    if flag_not_need_razdel:
                        continue

                    # if str(row[0]).startswith('Раздел 8'):
                    #     continue
                    # if str(row[0]).startswith('Раздел 6'):
                    #     continue

                    #######################

                elif str(row[0]).startswith(monocolumns):
                    if str(row[0]).startswith('4.6'):
                        if not data_table[idx_row + 2][1]:
                            continue
                    if not data_table[idx_row + 1][1]:
                        continue
                col_width = epw

                self.pdf.multi_cell(col_width, cell_h, str(row[0]), border=1, align=align_one_colun)






            else:
                self.pdf.set_font('PTSerif', '', 10)
                for idx, datum in enumerate(row):
                    col_width = epw / 2
                    if idx == 0:
                        if row[(idx + 1)]:
                            multicell_h_1 = check_cell_h(row[(idx + 1)])

                            if multicell_h_1 <= check_cell_h(datum):
                                multicell_h_1 = cell_h

                            if multicell_h_1 > check_cell_h(datum):
                                if check_cell_h(datum) > cell_h:
                                    pass

                            if self.pdf.y + multicell_h_1 + self.pdf.b_margin * 2 > 297:
                                self.pdf.add_page()

                            # Save top coordinate
                            top = self.pdf.y

                            str_num = self.pdf.page_no()
                            # Calculate x position of next cell
                            offset = self.pdf.x + col_width

                            old_top = self.pdf.y
                            self.pdf.multi_cell(col_width, multicell_h_1, str(datum), border=1)
                            # print(multicell_h)

                            new_h2 = self.pdf.y - old_top

                            if str_num == self.pdf.page_no():
                                self.pdf.y = top
                            else:
                                self.pdf.page = str_num
                                self.pdf.y = top
                            # Move to computed offset
                            self.pdf.x = offset
                    else:
                        if datum:
                            multicell_h_2 = check_cell_h(row[(idx - 1)])
                            if multicell_h_2 == check_cell_h(datum):
                                multicell_h_2 = cell_h

                            if multicell_h_2 > check_cell_h(datum):
                                if check_cell_h(datum) > cell_h:
                                    while multicell_h_2 != check_cell_h(datum):
                                        datum = datum + '\r\n'
                                    multicell_h_2 = cell_h

                            self.pdf.multi_cell(col_width, multicell_h_2, str(datum), border=1)
                            # self.pdf.set_font('PTSerif', '', 10)
                            # pdf.ln(cell_h)

        ostatok_y = self.pdf.h - self.pdf.t_margin - self.pdf.b_margin - self.pdf.y
        if ostatok_y < (cell_h * 5) + (th * 2) + 7:
            self.pdf.add_page()

        podpis_y = self.pdf.y + 6
        self.pdf.y = podpis_y
        page_podpis = self.pdf.page_no()
        w_1_from_5 = (epw / 7) * 2
        w_2_from_5 = (epw / 7) * 3
        offset = self.pdf.x + w_2_from_5

        self.pdf.set_font('PTSerifBold', '', 12)

        before_line_width = self.pdf.line_width

        self.pdf.set_line_width(before_line_width + 0.2)

        # self.pdf.line(self.pdf.l_margin, podpis_y, 200, podpis_y)

        self.pdf.multi_cell(w_2_from_5, cell_h * 5, 'Врио начальника Управления', border=1, align='C')

        self.pdf.x = offset
        self.pdf.y = podpis_y
        self.pdf.multi_cell(w_1_from_5, cell_h * 5, '', border=1)
        self.pdf.x = offset + w_1_from_5
        self.pdf.y = podpis_y
        self.pdf.multi_cell(w_1_from_5, cell_h * 5, 'Т.А-М.Галбацов', border=1, align='C')

        self.pdf.set_font('PTSerif', '', 10)
        podpis_y = self.pdf.y
        self.pdf.multi_cell(w_2_from_5, th,
                            'должность уполномоченного лица органа(организации), осуществляющего выдачу разрешения на строительство',
                            border=1, align='C')
        h_new = self.pdf.y - podpis_y
        self.pdf.y = podpis_y
        offset = self.pdf.x + w_2_from_5
        self.pdf.x = offset
        self.pdf.multi_cell(w_1_from_5, h_new, 'подпись', border=1, align='C')
        self.pdf.x = offset + w_1_from_5
        self.pdf.y = podpis_y
        self.pdf.multi_cell(w_1_from_5, h_new, 'инициалы, фамилия', border=1, align='C')

        self.pdf.set_line_width(before_line_width)

        file_name_result = f"{INPUT_DATA.get('1.2')}_Разрешение.pdf"
        self.pdf.output(file_name_result, 'F')
        # self.pdf.output(f"Разрешение.pdf", 'F')

        self.pdf.close()
        self.pdf = PDF(orientation='P', unit='mm', format='A4')
        self.pdf.add_page()
        return file_name_result

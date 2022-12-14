import pandas as pd

columns = [
    '1.1. Дата разрешения на строительство',
    '1.2. Номер разрешения на строительство',
    '1.3. Наименование органа (организации)',
    '1.4. Срок действия настоящего разрешения',
    '1.5. Дата внесения изменений или исправлений',
    # '2.1. Сведения о физическом лице или индивидуальном предпринимателе',
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
    # '3.3. Адрес (местоположение) объекта капитального строительства',
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
    # '4.3. Сведения о градостроительном плане земельного участка',
    '4.3.X.1. Дата:',
    '4.3.X.2. Номер:',
    '4.3.X.3. Наименование органа, выдавшего градостроительный план земельного участка:',
    '4.4. Условный номер земельного участка (земельных участков) на утвержденной схеме расположения '
    'земельного участка или земельных участков на кадастровом плане территории (при необходимости)',
    # '4.5. Сведения о схеме расположения земельного участка или земельных участков на кадастровом плане '
    # 'территории',
    '4.5.1. Дата решения:',
    '4.5.2. Номер решения:',
    '4.5.3. Наименовании организации, уполномоченного органа или лица, принявшего решение об утверждении '
    'схемы расположения земельного участка или земельных участков:',
    # '4.6. Информация о документации по планировке территории',
    # '4.6.1. Сведения о проекте планировки территории',
    '4.6.1.X.1. Дата решения:',
    '4.6.1.X.2. Номер решения:',
    '4.6.1.X.3. Наименование организации, уполномоченного органа или лица, принявшего решение об утверждении '
    'проекта планировки территории:',
    # '4.6.2. Сведения о проекте межевания территории',
    '4.6.2.X.1. Дата решения:',
    '4.6.2.X.2. Номер решения:',
    '4.6.2.X.3. Наименовании организации, уполномоченного органа или лица, принявшего решение об утверждении '
    'проекта межевания территории:',
    # '5.1. Сведения о разработчике - индивидуальном предпринимателе',
    '5.1.1. Фамилия:',
    '5.1.2. Имя:',
    '5.1.3. Отчество',
    '5.1.4. ИНН:',
    '5.1.5. ОГРНИП:',
    # '5.2. Сведения о разработчике - юридическом лице',
    '5.2.1. Полное наименование',
    '5.2.2. ИНН:',
    '5.2.3. ОГРН:',
    '5.3. Дата утверждения (при наличии)',
    '5.4. Номер (при наличии)',
    # '5.5. Типовое архитектурное решение объекта капитального строительства, утвержденное для исторического '
    # 'поселения (при наличии)',
    '5.5.1. Дата:',
    '5.5.2. Номер:',
    '5.5.3. Наименование документа:',
    '5.5.4. Наименование уполномоченного органа, принявшего решение об утверждении типового архитектурного '
    'решения:',
    # '6.1. Сведения об экспертизе проектной документации',
    '6.1.X.1. Дата утверждения:',
    '6.1.X.2. Номер:',
    '6.1.X.3. Наименование органа или организации, 3выдавшей положительное заключение экспертизы проектной '
    'документации:',
    # '6.2. Сведения о государственной экологической экспертизе',
    '6.2.X.1. Дата утверждения:',
    '6.2.X.2. Номер:',
    '6.2.X.3. Наименование органа, утвердившего положительное заключение государственной экологической '
    'экспертизы:',
    # '6.3. Подтверждение соответствия вносимых в проектную документацию изменений требованиям, указанным '
    # 'в части 3.8 статьи 49 Градостроительного кодекса Российской Федерации',
    '6.3.1. Дата:',
    '6.3.2. Номер:',
    '6.3.3. Сведения о лице, утвердившем указанное подтверждение',
    # '6.4. Подтверждение соответствия вносимых в проектную документацию изменений требованиям, указанным '
    # 'в части 3.9 статьи 49 Градостроительного кодекса Российской Федерации',
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


def x_make_arr(input_column):
    res_x_columns = []
    for col_x in range(1, 6):
        res_x_columns.append(str(input_column).replace('X', str(col_x)))

    return res_x_columns


if __name__ == '__main__':
    res_colums = []
    for col_ in columns:
        temp_str = str(col_).split()[0][:-1]
        if 'X' in temp_str:
            x_arr = x_make_arr(temp_str)
            res_colums += x_arr
        else:
            res_colums.append(temp_str)


    df = pd.DataFrame(columns=res_colums)

    INPUT_DATA = {'1.1': '06.09.2022г.', '1.2': '05-308-027-2022',
                  '1.3': 'Управление архитектуры и градостроительства Администрации города Махачкалы',
                  '1.4': '06.09.2024г.', '2.1.1': 'Пирмагомедов', '2.1.2': 'Разим', '2.1.3': 'Алифендиевич',
                  '2.1.4': '056006731592', '3.1': '4-х этажное торговое здание', '3.2': 'строительство',
                  '3.3.1': 'Республика Дагестан', '3.3.2': 'ГОсВД «город Махачкала»', '3.3.6': 'пр-кт Гамидова',
                  '3.3.7': 'уч.3, 3б', '4.1': '05:40:000060:14693', '4.2': '237 кв.м.', '4.3.1.1': '22.10.2021г.',
                  '4.3.1.2': 'РФ-05-2-01-1-00-2021-3417',
                  '4.3.1.3': 'Управление архитектуры и градостроительства Администрации города Махачкалы',
                  '5.2.1': 'ООО ПЦ «Инвест-Проект»', '5.2.2': '0571036001', '5.2.3': '1140571001064',
                  '6.1.1.1': '05.09.2022г.', '6.1.1.2': '05-2-1-3-063780-2022', '6.1.1.3': 'ООО «Коин-С»',
                  '7.1': '4-х этажное торговое здание', '7.1.1': 'здание', '7.1.2': 'нежилое', '7.1.3': '184.5',
                  '7.1.4': '657.97', '7.1.13': '4', '7.1.16': '15.95'}


    df_1 = pd.DataFrame({key: [value] for key, value in INPUT_DATA.items()})
    # df_2 = pd.DataFrame({'1.1': ['rrrr'], '1.3': 'fdsfds'})

    df = pd.concat([df, df_1])

    INPUT_DATA = {
        '1.1': '16.09.2022г.',
        '1.2': '05-40-028-2022',
        '1.3': 'Управление архитектуры и градостроительства Администрации города Махачкала',
        '1.4': '16.07.2024г.',
        '2.1.1': 'Будунов',
        '2.1.2': 'Магомед',
        '2.1.3': 'Каримулаевич',
        '2.1.4': '056000258002',
        '3.1': '13 этажный жилой дом со встроенно-пристроенными помещениями общественного назначения',
        '3.2': 'строительство',
        '3.3.1': 'Республика Дагестан',
        '3.3.2': 'ГОсВД «город Махачкала»',
        '3.3.6': 'пр-кт Насрутдинова',
        '3.3.7': 'в районе дома №50е',
        '4.1': '05:40:000069:10151',
        '4.2': '8 582 кв.м.',
        '4.3.1.1': '24.07.2020г.',
        '4.3.1.2': '05-308:000-3066',
        '4.3.1.3': 'Управление архитектуры и градостроительства Администрации города Махачкала',
        '5.2.1': 'ООО «Монтажспецстрой»',
        '5.2.2': '0544006230',
        '5.2.3': '1110544000050',
        '6.1.1.1': '19.04.2021г.',
        '6.1.1.2': '05-2-1-3-019197-2021',
        '6.1.1.3': 'ООО «Центр экспертизы и надзора строительства»',
        '7.1': '13 этажный жилой дом со встроенно-пристроенными помещениями общественного назначения',
        '7.1.1': 'здание',
        '7.1.2': 'жилое',
        '7.1.4': '2424,21',
        '7.1.5': '24136,92',
        '7.1.6': '3652,28',
        '7.1.7': '15745,75',
        '7.1.10': '179',
        '7.1.11': '179',
        '7.1.13': '14',
        '7.1.14': '1',
        '7.1.16': '45,703',
        '7.1.17': 'Решение Советского районного суда г.Махачкалы №2а-4875/2021, вступившее в законную силу 24.11.2021г. Исполнительное производство №109395/22/05022-ИП'
    }
    df_1 = pd.DataFrame({key: [value] for key, value in INPUT_DATA.items()})
    # df_2 = pd.DataFrame({'1.1': ['rrrr'], '1.3': 'fdsfds'})

    df = pd.concat([df, df_1])


    df.to_pickle('bd_test.pcl')

    print(df)
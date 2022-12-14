import pandas as pd


columns = [
    '1.1. Дата разрешения на ввод объекта в эксплуатацию:',
    '1.2. Номер разрешения на ввод объекта в эксплуатацию:',
    '1.3. Наименование органа (организации):',
    '1.4. Срок действия настоящего разрешения :',
    '1.5. Дата внесения изменений или исправлений :',
    '2.1.1. Фамилия:',
    '2.1.2. Имя:',
    '2.1.3. Отчество :',
    '2.1.4. ИНН:',
    '2.1.5. ОГРНИП :',
    '2.2.1. Полное наименование :',
    '2.2.2. ИНН:',
    '2.2.3. ОГРН:',
    '3.1. Наименование объекта капитального строительства (этапа) в соответствии с проектной документацией:',
    '3.2. Вид выполненных работ в отношении объекта капитального строительства:',
    '3.3.1. Субъект Российской Федерации:',
    '3.3.2. Муниципальный район, муниципальный округ, городской округ или внутригородская территория (для '
    'городов федерального значения) в составе субъекта Российской Федерации, федеральная территория:',
    '3.3.3. Городское или сельское поселение в составе муниципального района (для муниципального района) '
    'или внутригородского района городского округа (за исключением зданий, строений, сооружений, '
    'расположенных на федеральных территориях):',
    '3.3.4. Тип и наименование населенного пункта:',
    '3.3.5. Наименование элемента планировочной структуры:',
    '3.3.6. Наименование элемента улично-дорожной сети:',
    '3.3.7. Тип и номер здания (сооружения):',

    '4.1. Кадастровый номер земельного участка (земельных участков), в границах которого (которых) расположен объект капитального строительства:',
    '5.2. Номер разрешения на строительство:',
    '5.3. Наименование органа (организации), выдавшего разрешение на строительство:',
    '6.1. Наименование объекта капитального строительства, предусмотренного проектной документацией:',
    '6.1.1. Вид объекта капитального строительства:',
    '6.1.2. Назначение объекта:',
    '6.1.4. Площадь застройки (кв. м):',
    '6.1.4.1. Площадь застройки части объекта капитального строительства (кв. м):',
    '6.1.5. Площадь (кв. м):',
    '6.1.5.1. Площадь части объекта капитального строительства (кв. м) :',
    '6.1.6. Площадь нежилых помещений (кв. м):',
    '6.1.7. Общая площадь жилых помещений (с учетом балконов, лоджий, веранд и террас) (кв. м):',
    '6.1.8. Количество помещений (штук):',
    '6.1.9. Количество нежилых помещений (штук):',
    '6.1.10. Количество жилых помещений (штук):',
    '6.1.11. в том числе квартир (штук):',
    '6.1.12. Количество машино-мест (штук):',
    '6.1.13. Количество этажей:',
    '6.1.14. в том числе, количество подземных этажей:',
    '6.1.15. Вместимость (человек):',
    '6.1.16. Высота (м):',
    '6.1.17. Класс энергетической эффективности (при наличии):',
    '6.1.18. Иные показатели :',
    '6.1.19. Дата подготовки технического плана:',
    '6.1.20. Страховой номер индивидуального лицевого счета кадастрового инженера, подготовившего технический план:',
    '7.1. Наименование линейного объекта, предусмотренного проектной документацией:',
    '7.1.1. Кадастровый номер реконструированного линейного объекта:',
    '7.1.2. Протяженность (м) :',
    '7.1.2.1. Протяженность участка или части линейного объекта (м):',
    '7.1.3. Категория (класс):',
    '7.1.4. Мощность (пропускная способность, грузооборот, интенсивность движения):',
    '7.1.5. Тип (кабельная линия электропередачи, воздушная линия электропередачи, кабельно-воздушная линия электропередачи), уровень напряжения линий электропередачи:',
    '7.1.6. Иные показатели :',
    '7.1.7. Дата подготовки технического плана:',
    '7.1.8. Страховой номер индивидуального лицевого счета кадастрового инженера, подготовившего технический план:'
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

    INPUT_DATA = {
        '1.1': '14.09.2022',
        '1.2': '05-40-016-2022',
        '1.3': 'Управление архитектуры и градостроительства Администрации города Махачкалы',
        '2.1.1': 'Султанмеджидова',
        '2.1.2': 'Султанат',
        '2.1.3': 'Фейзуддиновна',
        '2.1.4': '056111667603',
        '3.1': '4-х этажное здание магазина',
        '3.2': 'строительство',
        '3.3.1': 'Республика Дагестан',
        '3.3.2': 'ГОсВД «город Махачкала»',
        '3.3.6': 'ул. Котрова',
        '3.3.7': '108',
        '4.1': '05:40:000053:1320',
        '5.1': '11.05.2017',
        '5.2': '05-308-115-2017',
        '5.3': 'Управление по вопросам координации капитального строительства Администрации города Махачкалы',
        '6.1': '4-х этажное здание магазина',
        '6.1.1': 'здание',
        '6.1.2': 'нежилое',
        '6.1.4': '433',
        '6.1.5': '2078,5',
        '6.1.13': '5',
        '6.1.14': '1',
        '6.1.19': '25.03.2022',
        '6.1.20': '092-662-442-81'

    }

    df_1 = pd.DataFrame({key: [value] for key, value in INPUT_DATA.items()})
    # df_2 = pd.DataFrame({'1.1': ['rrrr'], '1.3': 'fdsfds'})

    df = pd.concat([df, df_1])


    df.to_pickle('bd_RNV.pcl')

    print(df)

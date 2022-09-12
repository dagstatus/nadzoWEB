import pandas as pd
import pickle


file_settings = 'base_nadzor/settings_nadzor/settings_db.txt'
# file_settings = 'settings_db.txt'

class SettingsNadzor:
    def __init__(self):
        self.settings_dict = None
        self.read_settings()
        self.settings_labes_dict = {
            'nadzor_name': 'Наименование ведомства',
            'nadzor_adres': 'Адрес ведомства',
            'nadzor_email': 'Электронная почта ведомства',
            'nadzor_tel': 'Телефон ведомства',
            'nadzor_doljnost': 'Должность подписанта',
            'nadzor_fio': 'Инициалы, фамилия подписанта'
        }

    def save_settings(self):
        try:
            file = open(file_settings, 'wb')
            pickle.dump(self.settings_dict, file)
            file.close()
            return True
        except Exception as e:
            print(e)
            return False

    def read_settings(self):
        try:
            file = open(file_settings, 'rb')
            self.settings_dict = pickle.load(file)
            file.close()
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    TestClass = SettingsNadzor()
    TestClass.settings_dict = {
        'nadzor_name': 'УПРАВЛЕНИЕ АРХИТЕКТУРЫ И ГРАДОСТРОИТЕЛЬСТВА',
        'nadzor_adres': '367000, РД, г.Махачкала, ул. Коркмасова, 18',
        'nadzor_email': 'e-mail: uaig.mah@mail.ru',
        'nadzor_tel': 'тел. (8722) 78-02-72',
        'nadzor_doljnost': 'Врио начальника Управления',
        'nadzor_fio': 'Т.А-М.Галбацов'
    }

    TestClass.save_settings()

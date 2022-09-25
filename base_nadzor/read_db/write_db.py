import pandas as pd
import sqlite3, datetime
import uuid

class WriteDB:
    def __init__(self):
        self.result = None
        self.con = sqlite3.connect('base_nadzor/read_db/NADZO_DB.db')

    def add_rsn_to_sql(self, dict_to_add: dict):
        dict_to_add['uid'] = str(uuid.uuid4())
        dict_to_add['date_write_to_db'] = datetime.datetime.now()
        dict_to_add['show_flag'] = 1
        dict_to_add['version'] = 1
        new_df = pd.DataFrame({key: [value] for key, value in dict_to_add.items()})
        try:
            new_df.to_sql('RSN', con=self.con, if_exists='append', index=False)
        except:
            df = pd.read_sql_query('select * from RSN', con=self.con)
            df_2 = pd.concat([df, new_df])
            df_2.to_sql(name='RSN', con=self.con, if_exists='replace', index=False)


    def edit_rns_sql(self, dict_to_edit: dict):
        uid_father = dict_to_edit.get('UID')
        version = dict_to_edit.get('version')
        show_false_father_script = """UPDATE RSN SET show_flag = 1 WHERE uid = 'd754c8e5-5a32-46eb-8d74-1e111ae196cc'"""

        cursor = self.con.cursor()




    def add_rsn_to_db(self, dict_to_add: dict):
        print('try write')
        df = pd.read_pickle('base_nadzor/read_db/bd_test.pcl')

        new_df = pd.DataFrame({key: [value] for key, value in dict_to_add.items()})

        df = pd.concat([df, new_df])
        print(df)

        df.to_pickle('base_nadzor/read_db/bd_test.pcl')

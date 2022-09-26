import pandas as pd
import sqlite3, datetime
import uuid
import sqlalchemy


class WriteDB:
    def __init__(self):
        self.result = None
        # self.con = sqlite3.connect('base_nadzor/read_db/NADZO_DB.db')
        self.engine = sqlalchemy.create_engine('sqlite:///base_nadzor/read_db/NADZO_DB.db')


    def add_rsn_to_sql(self, dict_to_add: dict):
        dict_to_add['uid'] = str(uuid.uuid4())
        dict_to_add['date_write_to_db'] = datetime.datetime.now()
        dict_to_add['show_flag'] = 1
        dict_to_add['version'] = 1
        new_df = pd.DataFrame({key: [value] for key, value in dict_to_add.items()})
        try:
            new_df.to_sql('RSN', con=self.engine, if_exists='append', index=False)
        except:
            df = pd.read_sql_query('select * from RSN', con=self.con)
            df_2 = pd.concat([df, new_df])
            df_2.to_sql(name='RSN', con=self.engine, if_exists='replace', index=False)


    def edit_rns_sql(self, dict_new: dict, uid_father='', version=1):
        uid_father = uid_father
        show_false_father_script = f"""UPDATE RSN SET show_flag = 1 WHERE uid = '{uid_father}'"""

        dict_new['uid'] = str(uuid.uuid4())
        dict_new['date_write_to_db'] = datetime.datetime.now()
        dict_new['show_flag'] = 1
        dict_new['version'] = int(version) + 1

        cursor = self.con.cursor()
        cursor.execute(show_false_father_script)
        self.con.commit()
        new_df = pd.DataFrame({key: [value] for key, value in dict_new.items()})

        try:
            new_df.to_sql('RSN', con=self.con, if_exists='append', index=False)
        except:
            df = pd.read_sql_query('select * from RSN', con=self.con)
            df_2 = pd.concat([df, new_df])
            df_2.to_sql(name='RSN', con=self.con, if_exists='replace', index=False)



    def read_rns_db(self):
        df = pd.read_sql('select * from RSN', con=self.engine)

        return df

    def read_rnv_db(self):
        df = pd.read_sql('select * from RNV', con=self.engine)

        return df

    def add_rsn_to_db(self, dict_to_add: dict):
        print('try write')
        df = pd.read_pickle('base_nadzor/read_db/bd_test.pcl')

        new_df = pd.DataFrame({key: [value] for key, value in dict_to_add.items()})

        df = pd.concat([df, new_df])
        print(df)

        df.to_pickle('base_nadzor/read_db/bd_test.pcl')

import pandas as pd
import sqlite3


class WriteDB:
    def __init__(self):
        self.result = None

    def add_rsn_to_db(self, dict_to_add: dict):
        print('try write')
        df = pd.read_pickle('base_nadzor/read_db/bd_test.pcl')

        new_df = pd.DataFrame({key: [value] for key, value in dict_to_add.items()})

        df = pd.concat([df, new_df])
        print(df)

        df.to_pickle('base_nadzor/read_db/bd_test.pcl')

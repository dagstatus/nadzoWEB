import pandas as pd
import sqlite3

class SqlDB:
    def __init__(self):
        self.con = sqlite3.connect('base_nadzor/read_db/NADZO_DB.db')

    def read_rns_db(self):
        df = pd.read_sql_query('select * from RSN', con=self.con)
        self.con.close()
        return df

    def read_rnv_db(self):
        df = pd.read_sql_query('select * from RNV', con=self.con)
        self.con.close()
        return df



class ReadPandasRNS:
    def __init__(self):
        self.result = None

    def read_db(self):
        return pd.read_pickle('base_nadzor/read_db/bd_test.pcl')

class ReadpandasRNV:
    def __init__(self):
        self.result = None

    def read_db_rnv(self):
        return pd.read_pickle('base_nadzor/read_db/bd_RNV.pcl')
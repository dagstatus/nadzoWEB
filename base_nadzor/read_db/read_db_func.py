import pandas as pd

class ReadPandasRNS:
    def __init__(self):
        self.result = None

    def read_db(self):
        return pd.read_pickle('base_nadzor/read_db/bd_test.pcl')
import pandas as pd
from db_connection import database_connection
from constants import TABLE_NAME

input = pd.read_csv("Adressen__Berlin.csv")

columns_to_keep = [s for s in input.columns if len(input[s].unique())>1] #  Assumption that columns with only a single entry or with no entries don't contain any useful information

df_to_store = input[columns_to_keep]

df_to_store = df_to_store.drop(['OBJECTID_1'], axis = 1)

with database_connection('example.db') as db:
    db.store_dataframe_as_table(df_to_store, TABLE_NAME)

class Importer:
    def post(self):
        pass

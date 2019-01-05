import sqlite3 as s3
import pandas as pd

class database_connection:
    def __init__(self, name):
        self.db_name = name

    def __enter__(self):
        self.conn = s3.connect(self.db_name)

    def __exit__(self):
        self.conn.close()

    def get_query_as_dataframe(query):
        n = pd.read_sql_query(query, self.conn)
        return n

    def store_dataframe_as_table(self, frame_in, name, exists='replace'):
        frame_in.to_sql(name, self.conn, if_exists= exists)
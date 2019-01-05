import sqlite3 as s3

class database_connection:
    def __init__(self, name):
        self.db_name = name

    def __enter__(self):
        self.conn = s3.connect(self.db_name)

    def __exit__(self):
        self.conn.close()

    def get_query_as_dataframe(query):
        n = pd.read_sql_query(query, self.conn)
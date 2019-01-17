def import_addresses_to_database():
    import pandas as pd
    import numpy as np
    from pprint import pprint
    from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

    def _get_type(value_in):
        if isinstance(value_in, np.int_):
            return Integer
        else:
            return String(100)

    data = pd.read_csv("/home/diarmaid/PycharmProjects/Solvemate/application/Adressen__Berlin.csv")

    engine = create_engine('sqlite:///application/instance/foo.db')

    metadata = {}
    col_to_drop = ['OBJECTID_1']
    col_to_keep = []
    for a in data.columns:
        if len(data[a].unique()) == 1:
            metadata[a] = data[a].iloc[0]
            col_to_drop.append(a)
        else:
            col_to_keep.append(a)

    pprint([type(v) for k, v in metadata.items()])
    data.drop(columns=col_to_drop, inplace=True, axis=1)
    meta = MetaData(engine)

    cols = []
    for a in data.columns:
        cols.append(Column(a, _get_type(data[a].iloc[0]), primary_key=a == "OBJECTID"))

    addresses = Table("addresses", meta, *cols)

    print(data.columns)
    print(cols)
    data.to_sql("addresses", engine, if_exists="replace")
    print("done")
    other_data = pd.read_sql("addresses", engine)
    print(other_data.head())

if __name__ == "__main__":
    import_addresses_to_database()
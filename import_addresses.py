import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from os import makedirs


def _get_type(value_in):
    if isinstance(value_in, np.int_):
        return Integer
    else:
        return String(100)


def import_addresses_to_database(filepath = None):
    if filepath is None:
        filepath = 'Addresses__Berlin.csv'

    data = pd.read_csv(filepath)

    relative_path = 'instance'
    try:
        makedirs(relative_path)
    except OSError:
        pass

    engine = create_engine('sqlite:///instance/foo.db')

    col_to_drop = ['OBJECTID_1']
    for a in data.columns:
        if len(data[a].unique()) <= 1:
            col_to_drop.append(a)
    data.drop(columns=col_to_drop, inplace=True, axis=1)

    data.to_sql("addresses", engine, if_exists="replace")

if __name__ == "__main__":
    import_addresses_to_database()
import os
import tempfile

import pytest
from context import application
from sqlalchemy import Table, Column, Integer, String
import pandas as pd

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = application.create_application({
        'TESTING': True,
        'DATABASE': 'sqlite:////' + db_path,
    })

    client = app.test_client()
    context = app.app_context()
    with app.app_context() as con:
        engine, meta = application.get_buildings.get_db_engine_and_metadata()
        addresses = Table('addresses', meta,
                     Column('id', Integer, primary_key=True),
                     Column('PLZ', Integer, nullable=False),
                     Column('STR_DATUM', String(60), nullable=False),
                     )
        values = [{
            "PLZ": 10247,
            "id":1,
            'STR_DATUM': '1960-01-01T00:00:00'
        },
        {
            "PLZ": 10247,
            "id":2,
            'STR_DATUM': '1960-01-01T00:00:00'
        },
        {
            "PLZ": 10248,
            "id":3,
            'STR_DATUM': '1960-01-01T00:00:00'
        },
        {
            "PLZ": 10247,
            "id":4,
            'STR_DATUM': '1961-01-01T00:00:00'
        },
        {
            "PLZ": 10248,
            "id":5,
            'STR_DATUM': '1961-01-01T00:00:00'
        },
            {
            "PLZ": 10248,
            "id":6,
            'STR_DATUM': '1961-01-01T00:00:00'
        },
        {
            "PLZ": 10247,
            "id":1,
            'STR_DATUM': '1961-01-01T00:00:00'
        },
        ]
        data = pd.DataFrame(values)
        data.to_sql('addresses', engine, if_exists='replace')


    context.push()

    yield client

    context.pop()
    os.close(db_fd)
    os.unlink(db_path)


#@pytest.fixture
#def client(app):
#    return app.test_client()
#
#
#@pytest.fixture
#def runner(app):
#    return app.test_cli_runner()
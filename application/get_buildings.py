from flask import g
from flask_restful import Resource
from sqlalchemy import create_engine, MetaData, Table, func
from sqlalchemy.sql import select
from collections import Counter
import json

def get_db_engine_and_metadata():
    if 'engine' not in g:
        g.engine = create_engine('sqlite:///foo.db')
    if 'meta' not in g:
        g.meta = MetaData(bind=g.engine)
    return g.engine, g.meta


def get_table(name):
    engine, meta = get_db_engine_and_metadata()
    address_table = Table(name, meta, autoload=True, autoload_with=engine)
    return address_table


class addresses(Resource):
    def get(self, zip=None):
        engine, meta = get_db_engine_and_metadata()
        address_table = Table('addresses', meta, autoload=True, autoload_with=engine)
        s = select([address_table.c.PLZ])
        if zip:
            s = s.where(address_table.c.PLZ == zip)
        c = Counter([r[0] for r in engine.execute(s)])
        return json.dumps(c), 200


class added(Resource):
    def get(self, zip = None):
        engine, meta = get_db_engine_and_metadata()
        address_table = Table('addresses', meta, autoload=True, autoload_with=engine)
        s = select([address_table.c.STR_DATUM, func.count(address_table.c.PLZ)], group_by = address_table.c.STR_DATUM)
        if zip:
            s = s.where(address_table.c.PLZ == zip)
        results = {r[0]: r[1] for r in engine.execute(s)}
        return json.dumps(results), 200


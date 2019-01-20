from flask import g
from flask_restful import Resource
from sqlalchemy import create_engine, MetaData, Table, func
from sqlalchemy.sql import select
from collections import Counter
import json
from flask import current_app
import datetime


def get_db_engine_and_metadata():
    if 'engine' not in g:
        g.engine = create_engine(current_app.config['DATABASE'])
    if 'meta' not in g:
        g.meta = MetaData(bind=g.engine)
    return g.engine, g.meta


def get_table(name):
    engine, meta = get_db_engine_and_metadata()
    address_table = Table(name, meta, autoload=True, autoload_with=engine)
    return address_table


class Addresses(Resource):
    def get(self, zip=None):
        """Returns in JSON format a dictionary of zip: number of buildings. Filterable to a single zip"""
        engine, meta = get_db_engine_and_metadata()
        address_table = Table('addresses', meta, autoload=True, autoload_with=engine)
        s = select([address_table.c.PLZ])
        if zip:
            s = s.where(address_table.c.PLZ == zip)
        c = dict(Counter([r[0] for r in engine.execute(s)]))
        return json.dumps(c), 200


class GetNumAddedPerYear(Resource):
    def get(self, zip=None):
        """Returns in JSON format a dictionary of year: number of buildings. Filterable by zip."""
        engine, meta = get_db_engine_and_metadata()
        address_table = Table('addresses', meta, autoload=True, autoload_with=engine)
        s = select([address_table.c.STR_DATUM, func.count(address_table.c.PLZ)], group_by=address_table.c.STR_DATUM)
        if zip:
            s = s.where(address_table.c.PLZ == zip)
        results = {datetime.datetime.strptime(r[0], '%Y-%m-%dT%H:%M:%S').year: r[1] for r in engine.execute(s)}
        return json.dumps(results), 200
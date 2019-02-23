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


class Addresses(Resource):

    def get(self, zip_in=None):
        engine, meta = get_db_engine_and_metadata()
        address_table = Table('addresses', meta, autoload=True, autoload_with=engine )
        s = select([address_table.c.PLZ])
        if zip_in:
            s = s.where(address_table.c.PLZ == zip_in)
        c = dict(Counter([r[0] for r in engine.execute(s)]))
        return json.dumps(c), 200


class GetNumAddedPerYear(Resource):
    def get(self, zip_in=None):
        """Returns in JSON format a dictionary of
        year: number of buildings.
        Filterable by zip."""
        engine, meta = get_db_engine_and_metadata()
        address_table = Table('addresses', meta, autoload=True, autoload_with=engine)
        s = select([address_table.c.STR_DATUM, func.count(address_table.c.PLZ)], group_by=address_table.c.STR_DATUM)
        if zip_in:
            s = s.where(address_table.c.PLZ == zip_in)
        results = {r[0]: r[1] for r in engine.execute(s)}
        summed_results = {}
        for r, v in results.items():
            year = datetime.datetime.strptime(r, '%Y-%m-%dT%H:%M:%S').year
            summed_results[year] = summed_results.get(year, 0) + v
        return json.dumps(summed_results), 200

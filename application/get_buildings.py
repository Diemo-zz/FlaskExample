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



class addresses(Resource):
    def get(self, zip = None):
        engine, meta = get_db_engine_and_metadata()
        meta = MetaData(bind=engine)
        addresses = Table('addresses', meta, autoload=True, autoload_with=engine)
        s = select([addresses.c.PLZ])
        if zip:
            s = s.where(addresses.c.PLZ == zip)
        c = Counter([r[0] for r in engine.execute(s)])
        return json.dumps(c), 200

class added(Resource):
    def get(self, zip = None):
        engine, meta = get_db_engine_and_metadata()
        addresses = Table('addresses', meta, autoload=True, autoload_with=engine)
        s = select([addresses.c.STR_DATUM, func.count(addresses.c.PLZ)], group_by = addresses.c.STR_DATUM)
        if zip:
            print("ZIP")
            s = s.where(addresses.c.PLZ == zip)
        results = {r[0]: r[1] for r in engine.execute(s)}
        return json.dumps(results), 200

    #if zip:
    #    s = s.where(addresses.c.PLZ == zip)
    #    query = """select STR_DATUM, count() from addresses where PLZ = {0} group by STR_DATUM""".format(zip)
    #else:
    #    query = """select STR_DATUM, count() from addresses group by STR_DATUM"""
    #engine = get_db_engine_and_metadata()
    #df = engine.execute(query)
    #output = {"date_added": [],
    #          "number_of_buildings": []}
    #for r in df.fetchall():
    #    output["date_added"].append(r[0])
    #    output["number_of_buildings"].append(r[1])


from flask import g, current_app
from flask_restful import Resource
from sqlalchemy import create_engine, MetaData, Table, func
from sqlalchemy.sql import select
from collections import Counter
import json
import datetime


class UserActions(Resource):

    def get(self, id_or_name):
        """Returns the user """
        pass

    def put(self, id_or_name):
        pass

    def post(self, id_or_name):
        pass

    def delete(self, id_or_name):
        pass


class StorageActions(Resource):
    def get(self, id_or_name):
        """Returns the user """
        pass

    def put(self, id_or_name):
        pass

    def post(self, id_or_name):
        pass

    def delete(self, id_or_name):
        pass


class OrderActions(Resource):
    def get(self, id_or_name):
        """Returns the user """
        pass

    def put(self, id_or_name):
        pass

    def post(self, id_or_name):
        pass

    def delete(self, id_or_name):
        pass


class OrderLineActions(Resource):
    def get(self, id_or_name):
        """Returns the user """
        pass

    def put(self, id_or_name):
        pass

    def post(self, id_or_name):
        pass

    def delete(self, id_or_name):
        pass


class FulfilOrder(Resource):
    def get(self, order_id):
        pass

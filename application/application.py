from flask import Flask
from flask_restful import Api
from application.Endpoints.Initial import Initial
from application.Endpoints.Buildings import Buildings
from application.Endpoints.Time import Time
from application.importer import Importer
application = Flask(__name__)

api = Api(application)

api.add_resource(Initial, '/')

api.add_resource(Importer, '/importer')

api.add_resource(Buildings, '/buildings')

api.add_resource(Time, '/time')

if __name__ == "__main__":
    application.run()
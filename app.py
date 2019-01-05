from flask import Flask
from flask_restful import Api
from Endpoints.Initial import Initial
from Endpoints.Builings import Buildings
from importer import Importer
app = Flask(__name__)

api = Api(app)

api.add_resource(Initial, '/')

api.add_resource(Importer, '/importer')

api.add_resource(Buildings, '/buildings')

api.add_resource(Time, '/time')

if __name__ == "__main__":
    app.run()
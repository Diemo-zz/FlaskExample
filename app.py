from flask import Flask
from flask_restful import Resource, Api
from importer import Importer
app = Flask(__name__)

api = Api(app)

api.add_resource(Importer, '/')

if __name__ == "__main__":
    app.run()
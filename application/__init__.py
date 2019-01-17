from flask import Flask
import os
from flask_restful import Api
from sqlalchemy import create_engine
from .get_buildings import addresses, added




def create_application(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        engine = create_engine('sqlite:///instance/foo.db')
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    api = Api(app)

    api.add_resource(addresses, "/api/v1/number_of_buildings/<string:zip>", "/api/v1/number_of_buildings")
    api.add_resource(added, "/api/v1/added/<string:zip>", "/api/v1/added")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


if __name__ == "__main__":
    app = create_application()

from flask import Flask
import os
from flask_restful import Api
from .get_buildings import Addresses, GetNumAddedPerYear


def create_application(test_config=None):

    app = Flask(__name__.split('.')[0], instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
        if not app.config.get('DATABASE'):
            app.config['DATABASE'] = app.config.get('DATABASE_PREFIX', 'sqlite:///') + \
                                     os.path.join(app.instance_path, 'foo.db')
    else:
        app.config.from_mapping(test_config)

    api = Api(app)

    api.add_resource(Addresses, "/api/v1/number_of_buildings/<string:zip>", "/api/v1/number_of_buildings")
    api.add_resource(GetNumAddedPerYear, "/api/v1/added/<string:zip>", "/api/v1/added")

    return app


if __name__ == "__main__":
    app = create_application()

from flask import Flask
import os
from flask_restful import Api
from Initial import Initial

def create_application(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'Solvemate.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    api = Api(app)

    api.add_resource("/", Initial)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


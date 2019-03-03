from flask import Flask
import os
from flask_restful import Api
import application.model as model
import application.endpoints as endpoints
from application.database import database, migrate



def URI(text_in):
    return "/api/v1/"+text_in

def create_application(test_config=None):

    app = Flask(__name__.split('.')[0], instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if test_config is None:
        app.config.from_object('config.ProductionConfig')
        app.config.from_pyfile("config.py", silent=True)
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('DATABASE_PREFIX', 'sqlite:///') + \
                                     os.path.join(app.instance_path, 'foo.db')
    else:
        app.config.from_object(test_config)

    database.init_app(app)
    migrate.init_app(app, database)
    api = Api(app)

    with app.app_context():
        database.create_all()

    api.add_resource(endpoints.ProductActions, URI('user/<string:id_or_name>'))
    api.add_resource(endpoints.StorageActions, URI('storage/<string:id_or_name>'))
    api.add_resource(endpoints.OrderActions, URI('order/<string:id_or_name>'))
    api.add_resource(endpoints.OrderLineActions, URI('order/line/<string:id_or_name>'))
    api.add_resource(endpoints.FulfilOrder, URI('order/fufil/<string:order_id>'))

    return app


if __name__ == "__main__":
    app = create_application()

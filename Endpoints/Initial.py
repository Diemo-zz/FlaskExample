from flask_restful import Resource
class Initial(Resource):
    def get(self):
        return "Hello world"
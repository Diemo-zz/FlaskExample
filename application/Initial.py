from flask_restful import Resource

class Initial(Resource):
    def get(self):
        return "No", 200

    def post(self):
        return "Message is .. ", 200
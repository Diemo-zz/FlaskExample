from application.database import database


class Order(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String)

    def __init__(self, name):
        self.name = name

    def return_values(self):
        return {
            "id": self.id,
            "name": self.name
        }



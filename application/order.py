from application.database import database


class Order(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String)
    #order_line_id = database.Column(database.Integer, database.ForeignKey('OrderLine.id'))
    #order_line = database.relationship('OrderLine', backref="order")

    def __init__(self, name, product=None, quantity=None):
        self.name = name
        #if product is not None and quantity is not None:
        #    self.order = OrderLine(product, quantity)
        #else:
        #    self.order = None

    def return_values(self):
        return {
            "id": self.id,
            "name": self.name
        }



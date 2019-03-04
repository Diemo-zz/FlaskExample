from application.database import database


class OrderLine(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    #product_id = database.Column(database.Integer, database.ForeignKey('product.id'))
    #quantity = database.Column(database.Integer)
    #product = database.relationship('product')

    def __init__(self, product, quantity):
        pass
    #    self.product = product
    #    self.quantity = quantity

    def __repr__(self):
        return f"OrderLine: id: {self.id}"  # ", product: {self.product}, quantity = {self.quantity}"


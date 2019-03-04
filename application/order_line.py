from application.database import database


class OrderLine(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    quantity = database.Column(database.Integer)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'))
    product = database.relationship('Product')

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def __repr__(self):
        return f"OrderLine: id: {self.id}, product: {self.product}, quantity = {self.quantity}"

    def return_values(self):
        return {"product": self.product.name, "id": self.id, "quantity": self.quantity }


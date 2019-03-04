from application.database import database
from application.model import Product


class OrderLine(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    quantity = database.Column(database.Integer)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'))
    product = database.relationship('Product')

    def __init__(self, product_in, quantity):
        if isinstance(product_in, int):  # then this is the id to get
            product = Product.query.filter_by(id=product_in).first()
            if product is None:  # No product so we raise an error
                raise Exception
        elif isinstance(product_in, str):
            product = Product.query.filter_by(name=product_in).first()
            if product is None:  # we have the name so we can create it
                product = Product(product_in)
        elif isinstance(product_in, Product):
            product = product_in

        if not isinstance(product, Product):
            raise Exception

        self.product = product
        self.quantity = quantity

    def __repr__(self):
        return f"OrderLine: id: {self.id}, product: {self.product}, quantity = {self.quantity}"

    def return_values(self):
        return {"product": self.product.name, "id": self.id, "quantity": self.quantity }


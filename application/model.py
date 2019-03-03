from application.database import database
import json

class Storage(database.Model):
    #  __tablename__ = "storages"
    id = database.Column(database.Integer, primary_key=True)
    quantity = database.Column(database.Integer)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'))
    product = database.relationship('Product', backref='product')

    def init(self, quantity = 0, product='default_product'):
        if isinstance(product, int): # then this is the id to get
            product = Product.query.filter_by(id=product).first()
            if product is None:  # No product so we raise an error
                raise Exception
        elif isinstance(product, str):
            product = Product.query.filter_by(name=product).first()
            if product is None: # we have the name so we can create it
                product = Product(product)

        if not isinstance(product, Product):
            raise Exception

        self.product = product
        self.quantity = quantity





class Product(database.Model):
    #__tablename__ = "product"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String)
    storage = database.relationship('Storage')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Product %r>' % self.name

    def return_values(self):
        return dict(name=self.name, id=self.id)




#class Order(database.Model):
#    #  __tablename__ = "orders"
#    id = database.Column(database.Integer, primary_key=True)
#    name = database.Column(database.String)
#    order_line_id = database.Column(database.Integer, database.ForeignKey('OrderLine.id'))
#    order_line = database.relationship('OrderLine')
#
#
#class OrderLine(database.Model):
#    #  __tablename__ = "order_lines"
#    id = database.Column(database.Integer, primary_key=True)
#    product_id = database.Column(database.Integer, database.ForeignKey('Product.id'))
#    product = database.relationship('product')

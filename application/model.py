from application.database import database
import json


class Product(database.Model):
    #  __tablename__ = "product"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String)
    #storage = database.relationship('storage')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Product %r>' % self.name

    def return_values(self):
        return dict(name=self.name, id=self.id)


#class Storage(database.Model):
#    #  __tablename__ = "storages"
#    id = database.Column(database.Integer, primary_key=True)
#    quantity = database.Column(database.Integer)
#    product_id = database.Column(database.Integer, database.ForeignKey('Product.id'))
#    product = database.relationship('product')


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

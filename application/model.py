from application import db


class Product(db.Model):
    __tablename__ = "skus"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Storage(db.Model):
    __tablename__ = "storages"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'))
    product = db.relationship('Product')


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    order_line_id = db.Column(db.Integer, db.ForeignKey('OrderLine.id'))
    order_line = db.relationship('OrderLine')


class OrderLine(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'))
    product = db.relationship('Product')

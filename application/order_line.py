from application.database import database


class OrderLine(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    product_id = database.Column(database.Integer, database.ForeignKey('Product.id'))
    product = database.relationship('product')

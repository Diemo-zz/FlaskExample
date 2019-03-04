from application.database import database


class Order(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String)
    order_line_id = database.Column(database.Integer, database.ForeignKey('OrderLine.id'))
    order_line = database.relationship('OrderLine')



from flask_restful import Resource
from flask import request
from application.model import Product
from application.order import Order
from application.order_line import OrderLine
from application.database import database


class ProductActions(Resource):

    def get(self, id_or_name):
        """Returns the user """
        res = Product.query.filter_by(name=id_or_name).all()
        return [r.return_values() for r in res], 200

    def put(self, id_or_name):
        body = request.get_json()
        new_name = body.get('name')
        product = Product.query.filter_by(id=id_or_name).first()
        if product is None:
            return {"message": "No product to update! Use POST to create a new product"}, 404
        product.name = new_name
        database.session.add(product)
        database.session.commit()
        return {"message": "Success"}, 200

    def post(self, id_or_name):
        new_product = Product(id_or_name)
        database.session.add(new_product)
        database.session.commit()
        return new_product.id, 200

    def delete(self, id_or_name):
        product = Product.query.filter_by(id=id_or_name).first()
        if product is None:
            return {"message": "No product of that id to delete"}, 404
        database.session.delete(product)
        database.session.commit()
        return {"message": "Success"}, 200


class OrderActions(Resource):
    def get(self, id_or_name):
        """Returns the user """
        res = Order.query.filter_by(name=id_or_name).all()
        return [r.return_values() for r in res], 200

    def put(self, id_or_name):
        body = request.get_json()
        new_name = body.get('name')
        order = Order.query.filter_by(id=id_or_name).first()
        if order is None:
            return {"message": "No product to update! Use POST to create a new product"}, 404
        order.name = new_name
        database.session.add(order)
        database.session.commit()
        return {"message": "Success"}, 200

    def post(self, id_or_name):
        new_order = Order(id_or_name)
        database.session.add(new_order)
        database.session.commit()
        return new_order.id, 200

    def delete(self, id_or_name):
        order = Order.query.filter_by(id=id_or_name).first()
        if order is None:
            return {"message": "No order of that id to delete"}, 404
        database.session.delete(order)
        database.session.commit()
        return {"message": "Success"}, 200


class OrderLineActions(Resource):
    def get(self, id_or_name):
        """Returns the user """
        res = OrderLine.query.filter_by(id=id_or_name).all()
        return [r.return_values() for r in res], 200

    def put(self, id_or_name):
        body = request.get_json()
        product_name = body.get('product')
        quantity = body.get("quantity")
        order_line = OrderLine.query.filter_by(id=id_or_name).first()
        if order_line is None:
            return {"message": "No product to update! Use POST to create a new product"}, 404
        order_line.product.name = product_name
        if quantity is not None:
            order_line.quantity = quantity

        database.session.add(order_line)
        database.session.commit()
        return {"message": "Success"}, 200

    def post(self, id_or_name):
        body = request.get_json()
        product_name = id_or_name
        product = Product.query.filter_by(name=product_name).first()
        if product is None:
            product = Product(name=product_name)
        quantity = body.get("quantity")
        new_order_line = OrderLine(product, quantity)
        database.session.add(new_order_line)
        database.session.commit()
        return new_order_line.id, 200

    def delete(self, id_or_name):
        order = OrderLine.query.filter_by(id=id_or_name).first()
        if order is None:
            return {"message": "No order of that id to delete"}, 404
        database.session.delete(order)
        database.session.commit()
        return {"message": "Success"}, 200


class FulfilOrder(Resource):
    def get(self, order_id):
        pass

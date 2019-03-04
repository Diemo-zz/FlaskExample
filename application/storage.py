from flask_restful import Resource, request
from application.model import Storage, Product
from application.database import database


def get_product_from_FE_description(id_or_name):
    if isinstance(id_or_name, int) or str.isdigit(id_or_name):
        product = Product.query.filter_by(id=id_or_name).first()
    else:
        product = Product.query.filter_by(name=id_or_name).first()
    if product is None:
        product = Product(id_or_name)
    return product


class StorageActions(Resource):
    def get(self, id_or_name):
        """Returns the user """
        storage = Storage.query.filter_by(id=id_or_name).all()
        return [s.return_values() for s in storage], 200

    def put(self, id_or_name):
        data = request.get_json()
        storage = Storage.query.filter_by(id=id_or_name).first()
        if storage is None:
            return {"message": "No storage with that id found"}, 404
        if data.get('quantity'):
            storage.quantity = data.get('quantity')
        if data.get('product'):
            product = get_product_from_FE_description(data.get('product'))
            storage.product = product
        database.session.add(storage)
        database.session.commit()
        return {"message": "Success"}, 200

    def post(self, id_or_name):
        data = request.get_json()
        product = get_product_from_FE_description(id_or_name)
        quantity = data.get('quantity', 0)
        storage = Storage(quantity=quantity, product_in=product)
        database.session.add(storage)
        database.session.commit()
        return storage.id, 200

    def delete(self, id_or_name):
        storage = Storage.query.filter_by(id=id_or_name).first()
        if storage is None:
            return {"message": "No storage of that id to delete"}, 404
        database.session.delete(storage)
        database.session.commit()
        return {"message": "Success"}, 200



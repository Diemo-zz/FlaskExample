from application.database import database


class Storage(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    quantity = database.Column(database.Integer)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'))
    product = database.relationship('Product', backref='product')

    def __init__(self, quantity=0, product_in='default_product'):
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
        print(self.product, product)

    def __repr__(self):
        return "Storage {id} holding {q} of product {p}".format(id=self.id, q=self.quantity, p=self.product)

    def return_values(self):
        return dict(id=self.id, product=self.product.name, product_id=self.product.id, quantity=self.quantity)


class Product(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String)
    storage = database.relationship('Storage')
    order = database.relationship('OrderLine')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Product %r>' % self.name

    def return_values(self):
        return dict(name=self.name, id=self.id)

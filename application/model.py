from application.database import database


class Storage(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    quantity = database.Column(database.Integer)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'))
    product = database.relationship('Product', backref='product')

    def init(self, quantity=0, product='default_product'):
        if isinstance(product, int):  # then this is the id to get
            product = Product.query.filter_by(id=product).first()
            if product is None:  # No product so we raise an error
                raise Exception
        elif isinstance(product, str):
            product = Product.query.filter_by(name=product).first()
            if product is None:  # we have the name so we can create it
                product = Product(product)

        if not isinstance(product, Product):
            raise Exception
        print(self.product)

        self.product = product
        self.quantity = quantity

    def __repr__(self):
        print(self.id)
        return "Storage {id} holding {q} of product {p}".format(id=self.id, q=self.quantity, p=self.product)

    def return_values(self):
        return dict(id=self.id, product=self.product.name, product_id=self.product.id, quantity=self.quantity)


class Product(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String)
    storage = database.relationship('Storage')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Product %r>' % self.name

    def return_values(self):
        return dict(name=self.name, id=self.id)

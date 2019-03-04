import unittest
from application import create_application
from application.config import TestingConfig
from application.database import database
from application.model import Product, Storage
import json


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_application(TestingConfig)
        with self.app.app_context():
            database.create_all()

    def test_get_storage_with_no_storage(self):
        with self.app.test_client() as c:
            res = c.get('/api/v1/storage/1')
            self.assertEqual(res.status_code, 200)
            self.assertListEqual(json.loads(res.data), [])

    def test_get_storage_with_storage(self):
        with self.app.app_context():
            p = Product("new product")
            s = Storage(quantity=10, product=p)
            database.session.add(s)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.get('/api/v1/storage/1')
            self.assertEqual(res.status_code, 200)
            expected_results = [{
                'quantity': 10,
                'product': "new product",
                'product_id': 1,
                'id': 1
            }]
            self.assertListEqual(expected_results, json.loads(res.data))

    def test_creating_a_storage(self):
        with self.app.test_client() as c:
            res = c.post('api/v1/storage/product_name',
                         data=json.dumps(dict(quantity=2)),
                         content_type='application/json')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json.loads(res.data), 1)

        with self.app.app_context():
            storage = Storage.query.filter_by(id=1).first()
            self.assertEqual(storage.quantity, 2)

    def test_updating_a_storage_status_code_with_no_storage(self):
        with self.app.test_client() as c:
            res = c.put('api/v1/storage/{0}'.format(121),
                        data=json.dumps(dict(quantity=6)),
                        content_type='application/json')
            self.assertEqual(res.status_code, 404)

    def test_updating_a_storage_changing_quantity(self):
        with self.app.app_context():
            prod = Product("product")
            storage = Storage(quantity=0, product=prod)
            database.session.add(storage)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.put('api/v1/storage/1',
                        data=json.dumps(dict(quantity=10)),
                        content_type='application/json')
            self.assertEqual(res.status_code, 200)
        with self.app.app_context():
            storage = Storage.query.filter_by(id=1).first()
            self.assertEqual(storage.quantity, 10)

    def test_updating_a_storage_changing_product(self):
        with self.app.app_context():
            prod = Product("product")
            prod2 = Product("second product")
            storage = Storage(quantity=0, product=prod)
            database.session.add(storage)
            database.session.add(prod2)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.put('api/v1/storage/1',
                        data=json.dumps(dict(quantity=10, product=2)),
                        content_type='application/json')
            self.assertEqual(res.status_code, 200)
        with self.app.app_context():
            storage = Storage.query.filter_by(id=1).first()
            self.assertEqual(storage.product.name, "second product")

    def test_deleteing_a_storage_when_storage_is_there_status_code(self):
        product = Product("name")
        storage = Storage(quantity=2, product=product)
        with self.app.app_context():
            database.session.add(storage)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.delete('/api/v1/storage/1')
            self.assertEqual(res.status_code, 200)
        with self.app.app_context():
            s = Storage.query.filter_by(id=1).first()
            self.assertIsNone(s)

    def test_deleteing_a_storage_when_storage_is_not_there_status_code(self):
        with self.app.test_client() as c:
            res = c.delete('/api/v1/user/1')
            self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()

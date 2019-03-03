import unittest
from application import create_application
from application.config import TestingConfig
from application.database import database
from application.model import Product
import json


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_application(TestingConfig)
        with self.app.app_context():
            database.create_all()

    def test_get_product_with_no_product_status_code(self):
        with self.app.test_client() as c:
            res = c.get('/api/v1/user/no_user_found')
            self.assertEqual(res.status_code, 200)

    def test_get_product_with_no_product_results(self):
        with self.app.test_client() as c:
            res = c.get('/api/v1/user/no_user_found')
            self.assertListEqual(json.loads(res.data), [])

    def test_creating_a_product_status_code(self):
        with self.app.test_client() as c:
            res = c.post('api/v1/user/created_user')
            self.assertEqual(res.status_code, 200)

    def test_creating_a_products_return_values(self):
        with self.app.test_client() as c:
            res = c.post('api/v1/user/created_user')
            expected = 1
            self.assertEqual(json.loads(res.data), expected)


    def test_creating_and_retrieving_a_product(self):
        test_user = "test_user"
        with self.app.test_client() as c:
            c.post('api/v1/user/{0}'.format(test_user))
            res = c.get('api/v1/user/test_user')
            expected = [{
                "id": 1,
                "name": test_user
            }]
            self.assertListEqual(expected, json.loads(res.data))

    def test_updating_a_product_status_code_with_no_product(self):
        with self.app.test_client() as c:
            res = c.put('api/v1/user/{0}'.format(121),
                        data=json.dumps(dict(name='new_product')),
                        content_type='application/json')
            self.assertEqual(res.status_code, 404)

    def test_updating_a_product_status_code(self):
        product = "initial_name"
        with self.app.test_client() as c:
            id = c.post('api/v1/user/{0}'.format(product))
            res = c.put('api/v1/user/{0}'.format(json.loads(id.data)),
                        data=json.dumps(dict(name='new_product')),
                        content_type='application/json')
            self.assertEqual(res.status_code, 200)

    def test_updating_a_product_name(self):
        product = "test_product"
        new_name = "new_name"
        with self.app.test_client() as c:
            id = c.post('api/v1/user/{0}'.format(product))
            res = c.put('api/v1/user/{0}'.format(json.loads(id.data)),
                        data=json.dumps(dict(name=new_name)),
                        content_type='application/json')
            product = Product.query.filter_by(name=new_name).first()
            self.assertEqual(product.name, new_name)
            self.assertEqual(res.status_code, 200)

    def test_deleteing_a_product_when_product_is_there_status_code(self):
        product = Product("name")
        with self.app.app_context():
            database.session.add(product)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.delete('/api/v1/user/1')
            self.assertEqual(res.status_code, 200)

    def test_deleteing_a_product_when_product_is_not_there_status_code(self):
        product = Product("name")
        with self.app.test_client() as c:
            res = c.delete('/api/v1/user/1')
            self.assertEqual(res.status_code, 404)

    def test_deleteing_a_product_when_product_is_there_deletion_works(self):
        product = Product("name")
        with self.app.app_context():
            database.session.add(product)
            database.session.commit()
        with self.app.test_client() as c:
            c.delete('/api/v1/user/1')
        with self.app.app_context():
            res = Product.query.filter_by(id=1).first()
            self.assertIsNone(res)




if __name__ == '__main__':
    unittest.main()

import unittest
from application import create_application
from application.config import TestingConfig
from application.database import database
import json
from application.order import Order
from application.model import Product
from application.order_line import OrderLine


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_application(TestingConfig)
        with self.app.app_context():
            database.create_all()

    def test_get_orderline_with_no_order(self):
        with self.app.test_client() as c:
            res = c.get('/api/v1/order/line/2')
            self.assertEqual(res.status_code, 200)
            self.assertListEqual(json.loads(res.data), [])

    def test_get_orderline_with_orderline(self):
        with self.app.app_context():
            product = Product("product")
            o = OrderLine(product, 2)
            database.session.add(o)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.get('/api/v1/order/line/1')
            self.assertEqual(res.status_code, 200)
            expected = {
                "product": "product",
                "quantity": 2,
                "id": 1,
            }
            self.assertDictEqual(expected, json.loads(res.data)[0])

    def test_creating_an_orderline(self):
        with self.app.test_client() as c:
            res = c.post('api/v1/order/line/name',
                         data=json.dumps(dict(quantity=6)),
                         content_type='application/json')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json.loads(res.data), 1)

    def test_updating_a_orderline_status_code_with_no_orderline(self):
        with self.app.test_client() as c:
            res = c.put('api/v1/order/line/{0}'.format(121),
                        data=json.dumps(dict(quantity=6)),
                        content_type='application/json')
            self.assertEqual(res.status_code, 404)

    def test_updating_a_orderline_changing_quantity(self):
        with self.app.app_context():
            p = Product("newprod")
            ol = OrderLine(p, 10)
            database.session.add(ol)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.put('api/v1/order/line/1',
                        data=json.dumps(dict(quantity="6", product="otherprod")),
                        content_type='application/json')
            self.assertEqual(res.status_code, 200)
        with self.app.app_context():
            order = OrderLine.query.filter_by(id=1).first()
            self.assertEqual(order.product.name, "otherprod")
            self.assertEqual(order.quantity, 6)

    def test_deleteing_a_storage_when_storage_is_there_status_code(self):
        with self.app.app_context():
            p = Product("newprod")
            ol = OrderLine(p, 10)
            database.session.add(ol)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.delete('/api/v1/order/line/1')
            self.assertEqual(res.status_code, 200)
        with self.app.app_context():
            s = Order.query.filter_by(id=1).first()
            self.assertIsNone(s)

    def test_deleting_an_order_line_when_storage_is_not_there(self):
        with self.app.test_client() as c:
            res = c.delete('/api/v1/order/line/1')
            self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()

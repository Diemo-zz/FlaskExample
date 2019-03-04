import unittest
from application import create_application
from application.config import TestingConfig
from application.database import database
import json
from application.order import Order


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_application(TestingConfig)
        with self.app.app_context():
            database.create_all()

    def test_get_order_with_no_order(self):
        with self.app.test_client() as c:
            res = c.get('/api/v1/order/2')
            self.assertEqual(res.status_code, 200)
            self.assertListEqual(json.loads(res.data), [])

    def test_get_order_with_order(self):
        with self.app.app_context():
            o = Order("newname")
            database.session.add(o)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.get('/api/v1/order/newname')
            self.assertEqual(res.status_code, 200)
            expected = {
                "name": "newname",
                "id": 1,
            }
            self.assertDictEqual(expected, json.loads(res.data)[0])

    def test_creating_an_order(self):
        with self.app.test_client() as c:
            res = c.post('api/v1/order/name')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json.loads(res.data), 1)

    def test_updating_a_storage_status_code_with_no_storage(self):
        with self.app.test_client() as c:
            res = c.put('api/v1/order/{0}'.format(121),
                        data=json.dumps(dict(quantity=6)),
                        content_type='application/json')
            self.assertEqual(res.status_code, 404)

    def test_updating_a_oder_changing_name(self):
        with self.app.app_context():
            order = Order("oldname")
            database.session.add(order)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.put('api/v1/order/1',
                        data=json.dumps(dict(name="newname")),
                        content_type='application/json')
            self.assertEqual(res.status_code, 200)
        with self.app.app_context():
            order = Order.query.filter_by(id=1).first()
            self.assertEqual(order.name, "newname")

    def test_deleteing_a_storage_when_storage_is_there_status_code(self):
        order = Order(name="Ordername")
        with self.app.app_context():
            database.session.add(order)
            database.session.commit()
        with self.app.test_client() as c:
            res = c.delete('/api/v1/order/1')
            self.assertEqual(res.status_code, 200)
        with self.app.app_context():
            s = Order.query.filter_by(id=1).first()
            self.assertIsNone(s)


if __name__ == '__main__':
    unittest.main()

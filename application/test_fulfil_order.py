import unittest
from application import create_application
from application.config import TestingConfig
from application.database import database
import json


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_application(TestingConfig)
        with self.app.app_context():
            database.create_all()

    def test_get_orderline_with_no_order(self):
        body = { "lines": [ {
                             "sku": 'abc', "quantity": 12 }, { "sku": 'def', "quantity": 2 } ], "storages":
            [{
                    "id": 'zzz',
                    "sku": 'abc',
                    "quantity": 5
                },
                   {
                       "id": 'yyy',
                       "sku": 'abc',
                       "quantity": 100
                   },
               {
                   "id": 'xxx',
                   "sku": 'def',
                   "quantity": 100
               }]
        }
        with self.app.test_client() as c:
            res = c.get('/api/v1/order/fufil/2', data=json.dumps(body),
                        content_type='application/json')
            self.assertEqual(res.status_code, 200)
            self.assertListEqual(json.loads(res.data), [])


if __name__ == "__main__":
    unittest.main()

import unittest
from application.application import application

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(False, False)

    def setUp(self):
        self.application = application.test_client()

    def tearDown(self):
        pass

    def test_initial(self):
        response = self.application.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

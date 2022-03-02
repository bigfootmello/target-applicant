import unittest
from tests.base_setup import BaseTestCase


class APITestCase(BaseTestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)





if __name__ == "__main__":
    unittest.main()

import unittest
from tests.base_setup import BaseTestCase


class APITestCase(BaseTestCase):

    API_URL = "http://127.0.0.1:8000/"
    PRODUCT = {"Name": "Golf Club",
               "Description": "The one thing you always wanted but didn't know why",
               "SKU": "2258L09PL6913TR2",
               "OnlineOnly": False,
               "InStoreOnly": False}

    def test_a_index(self):
        response = self.client.get(APITestCase.API_URL)
        self.assertEqual(response.status_code, 200)

    # def test_b_get_product(self):
    #     response = self.client.get(APITestCase.API_URL + "api/product/quick")
    #     self.assertEqual(response.status_code, 200)

    # def test_c_add_product(self):
    #     response = self.client.put(APITestCase.API_URL + "api/product/589", json=APITestCase.PRODUCT)
    #     self.assertEqual(response.status_code, 201)

    # def test_update_product(self):  # Needs work, failing
    #     product_id = 2
    #     response = self.client.patch(API_URL + str(product_id), query_string={"Description": "Did I say soft? Oh, it's not"})
    #     self.assertEqual(response.status_code, 204)

    # def test_delete_product(self):
    #     product_id = 312
    #     response = self.client.delete(API_URL + str(product_id))
    #     self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()

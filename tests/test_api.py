import unittest
from tests.base_setup import BaseTestCase

API_URL = "http://127.0.0.1:8000/"
PRODUCT = {"Name": "Magic Eight Ball", "Description": "Making life decisions since 1946", "SKU": "1058L09PL6913TR2",
           "OnlineOnly": False, "InStoreOnly": False}


class APITestCase(BaseTestCase):

    def test_1_index(self):
        response = self.client.get(API_URL)
        self.assertEqual(response.status_code, 200)

    # def test_2_get_product(self):
    #     response = self.client.get(API_URL + "api/product/quick")
    #     self.assertEqual(response.status_code, 200)

    # def test_add_product(self):
    #     response = self.client.put(API_URL + "api/product/400", json=PRODUCT)
    #     self.assertEqual(response.status_code, 201)

    # def test_update_product(self):  # Needs work, failing
    #     product_id = 2
    #     response = self.client.patch(API_URL + str(product_id), query_string={"Description": "Did I say soft? Oh, it's not"})
    #     self.assertEqual(response.status_code, 204)

    # def test_5_delete_product(self):
    #     product_id = 312
    #     response = self.client.delete(API_URL + str(product_id))
    #     self.assertEqual(response.status_code, 204)






if __name__ == "__main__":
    unittest.main()

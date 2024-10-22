import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from routers.product_routes import router

class TestProductRoutes:

    @pytest.fixture(scope="module")
    def initialize_test_client(self):
        return TestClient(router)

    @pytest.mark.parametrize("input_data", [
        ({"name": "TestProduct1",
          "price": 22.5,
          "discount": 3,
          "category": "TestCategory1"}),
        ({"name": "TestProduct2",
          "price": 12.5,
          "discount": 0,
          "category": "TestCategory2"}),
        ({"name": "TestProduct3",
          "price": 32.0,
          "discount": 100,
          "category": "TestCategory3"})
    ])
    def test_create_product(self, initialize_test_client, input_data):

        initialize_test_client.delete(f"/{input_data['name']}")

        response = initialize_test_client.post("/", json=input_data)

        assert response.status_code == 200
        assert "oid" in response.json().keys()
        initialize_test_client.delete(f"/{input_data['name']}")

    @pytest.mark.parametrize("input_data",
                             [
                                 ({"name": "TestProduct1",
                                   "price": 22.5,
                                   "discount": 3,
                                   "category": "TestCategory1"}),
                                 ({"name": "TestProduct2",
                                   "price": 12.5,
                                   "discount": 0,
                                   "category": "TestCategory2"}),
                                 ({"name": "TestProduct3",
                                   "price": 32.0,
                                   "discount": 100,
                                   "category": "TestCategory3"})
                             ])
    def test_read_product(self, initialize_test_client, input_data):

        initialize_test_client.delete(f"/{input_data['name']}")

        response = initialize_test_client.post("/", json=input_data)

        response = initialize_test_client.get(f"/{input_data['name']}")

        assert response.status_code == 200
        assert response.json()["name"] == input_data["name"]
        assert response.json()["price"] == input_data["price"]
        assert response.json()["discount"] == input_data["discount"]
        assert response.json()["category"] == input_data["category"]
        initialize_test_client.delete(f"/{input_data['name']}")

    @pytest.mark.parametrize("input_data",
                             [
                                 ({"name": "TestProduct1",
                                   "price": 22.5,
                                   "discount": 3,
                                   "category": "TestCategory1"}),
                                 ({"name": "TestProduct2",
                                   "price": 12.5,
                                   "discount": 0,
                                   "category": "TestCategory2"}),
                                 ({"name": "TestProduct3",
                                   "price": 32.0,
                                   "discount": 100,
                                   "category": "TestCategory3"})
                             ])
    def test_read_product_exception_raise(self, initialize_test_client, input_data):
        initialize_test_client.delete(f"/{input_data['name']}")

        with pytest.raises(HTTPException) as exc_info:
            initialize_test_client.get(f"/{input_data['name']}")

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Product not found!"

    @pytest.mark.parametrize("input_data", [
        ([{"name": "TestProduct1.1",
           "price": 12.5,
           "discount": 2,
           "category": "TestCategory1.1"}]),
        ([{"name": "TestProduct2.1",
           "price": 22.5,
           "discount": 3,
           "category": "TestCategory2.1"},
          {"name": "TestProduct2.2",
           "price": 55.5,
           "discount": 7,
           "category": "TestCategory2.2"}]),
        ([{"name": "TestProduct3.1",
           "price": 41.5,
           "discount": 4,
           "category": "TestCategory3.1"},
          {"name": "TestProduct3.2",
           "price": 69.5,
           "discount": 96,
           "category": "TestCategory3.2"},
          {"name": "TestProduct3.3",
           "price": 73.8,
           "discount": 12,
           "category": "TestCategory3.3"},
          {"name": "TestProduct3.4",
           "price": 16.0,
           "discount": 100,
           "category": "TestCategory3.4"}
          ])
    ])
    def test_read_products(self, initialize_test_client, input_data):

        for product_data in input_data:
            initialize_test_client.delete(f"/{product_data['name']}")

        for product_data in input_data:
            response = initialize_test_client.post("/", json=product_data)

        response = initialize_test_client.get("/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == len(input_data)

        for i in enumerate(input_data):
            assert response.json()[i]["name"] == input_data[i]["name"]
            assert response.json()[i]["price"] == input_data[i]["price"]
            assert response.json()[i]["discount"] == input_data[i]["discount"]
            assert response.json()[i]["category"] == input_data[i]["category"]

        # assert response.json()[0]["name"] == products_data[0]["name"]
        # assert response.json()[0]["price"] == products_data[0]["price"]
        # assert response.json()[0]["discount"] == products_data[0]["discount"]
        # assert response.json()[0]["category"] == products_data[0]["category"]
        #
        # assert response.json()[1]["name"] == products_data[1]["name"]
        # assert response.json()[1]["price"] == products_data[1]["price"]
        # assert response.json()[1]["discount"] == products_data[1]["discount"]
        # assert response.json()[1]["category"] == products_data[1]["category"]

        for product_data in input_data:
            initialize_test_client.delete(f"/{product_data['name']}")

    @pytest.mark.parametrize("input_data",
                             [
                                 ({
                                     "reference_name": "TestProduct",
                                     "name": "TestProductUpdate1",
                                     "price": 55.5,
                                     "discount": 6,
                                     "category": "TestCategoryUpdate1"}),
                                 ({
                                     "reference_name": "TestProduct",
                                     "name": "TestProductUpdate2",
                                     "price": 14.5,
                                     "discount": 200,
                                     "category": "TestCategoryUpdate2"}),
                                 ({
                                     "reference_name": "TestProduct",
                                     "name": "TestProductUpdate3",
                                     "price": 65.5,
                                     "discount": 20,
                                     "category": "TestCategoryUpdate3"}),
                                 ({
                                     "reference_name": "TestProduct_NotExistent",
                                     "name": "TestProductUpdate4",
                                     "price": 40.5,
                                     "discount": 7,
                                     "category": "TestCategoryUpdate4"})
                             ]
                             )
    def test_update_product(self, initialize_test_client, input_data):
        product_data = {"name": "TestProduct",
                        "price": 12.5,
                        "discount": 2,
                        "category": "TestCategory"}
        initialize_test_client.delete(f"/{product_data['name']}")

        response = initialize_test_client.post("/", json=product_data)

        response = initialize_test_client.put(f"/{input_data['reference_name']}", json=input_data)

        assert response.status_code == 200
        del input_data["reference_name"]

        if response.json() != {
            "name": "Not Found",
            "price": 0.0,
            "discount": 0,
            "category": "Not Found"}:
            assert response.json() == input_data

        initialize_test_client.delete(f"/{input_data['name']}")

    @pytest.mark.parametrize("input_data",
                             [({"name": "TestProduct1",
                                "price": 24.5,
                                "discount": 6,
                                "category": "TestCategory1"}),
                              ({"name": "TestProduct",
                                "price": 43834.5,
                                "discount": 1,
                                "category": "TestCategory"}),
                              ({"name": "TestProduct",
                                "price": 43.5,
                                "discount": 44,
                                "category": "TestCategory"})])
    def test_delete_product(self, initialize_test_client, input_data):

        initialize_test_client.delete(f"/{input_data['name']}")

        response = initialize_test_client.post("/", json=input_data)

        response = initialize_test_client.delete(f"{input_data['name']}")

        assert response.status_code == 200
        assert response.json() is True

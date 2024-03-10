from routers.product_routes import router
from fastapi.testclient import TestClient

import pytest


class TestProductRoutes:

    @pytest.fixture(scope="module")
    def initialize_test_client(self):
        return TestClient(router)

    @pytest.mark.parametrize("input",[
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
    def test_create_product(self, initialize_test_client, input):

        initialize_test_client.delete(f"/{input['name']}")

        response = initialize_test_client.post("/", json=input)

        assert response.status_code == 200
        assert "oid" in response.json().keys()
        initialize_test_client.delete(f"/{input['name']}")

    @pytest.mark.parametrize("input",
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
    def test_read_product(self, initialize_test_client, input):

        initialize_test_client.delete(f"/{input['name']}")

        response = initialize_test_client.post("/", json=input)

        response = initialize_test_client.get(f"/{input['name']}")

        assert response.status_code == 200
        assert response.json()["name"] == input["name"]
        assert response.json()["price"] == input["price"]
        assert response.json()["discount"] == input["discount"]
        assert response.json()["category"] == input["category"]
        initialize_test_client.delete(f"/{input['name']}")

    @pytest.mark.parametrize("input", [
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
    def test_read_products(self, initialize_test_client, input):

        for product_data in input:
            initialize_test_client.delete(f"/{product_data['name']}")

        for product_data in input:
            response = initialize_test_client.post("/", json=product_data)

        response = initialize_test_client.get("/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == len(input)

        for i in range(0, len(input)):
            assert response.json()[i]["name"] == input[i]["name"]
            assert response.json()[i]["price"] == input[i]["price"]
            assert response.json()[i]["discount"] == input[i]["discount"]
            assert response.json()[i]["category"] == input[i]["category"]

        # assert response.json()[0]["name"] == products_data[0]["name"]
        # assert response.json()[0]["price"] == products_data[0]["price"]
        # assert response.json()[0]["discount"] == products_data[0]["discount"]
        # assert response.json()[0]["category"] == products_data[0]["category"]
        #
        # assert response.json()[1]["name"] == products_data[1]["name"]
        # assert response.json()[1]["price"] == products_data[1]["price"]
        # assert response.json()[1]["discount"] == products_data[1]["discount"]
        # assert response.json()[1]["category"] == products_data[1]["category"]

        for product_data in input:
            initialize_test_client.delete(f"/{product_data['name']}")

    @pytest.mark.parametrize("input",
                             [({
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
                                     "category": "TestCategoryUpdate3"})
                             ]
                             )
    def test_update_product(self, initialize_test_client, input):
        product_data = {"name": "TestProduct",
                        "price": 12.5,
                        "discount": 2,
                        "category": "TestCategory"}
        initialize_test_client.delete(f"/{product_data['name']}")

        response = initialize_test_client.post("/", json=product_data)

        response = initialize_test_client.put(f"/{input['reference_name']}", json=input)

        assert response.status_code == 200

        print(response.json())

        del input["reference_name"]
        assert response.json() == input

        initialize_test_client.delete(f"/{input['name']}")

    @pytest.mark.parametrize("input",
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
    def test_delete_product(self, initialize_test_client, input):

        initialize_test_client.delete(f"/{input['name']}")

        response = initialize_test_client.post("/", json=input)

        response = initialize_test_client.delete(f"{input['name']}")

        assert response.status_code == 200
        assert response.json() is True

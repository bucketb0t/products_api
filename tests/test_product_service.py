import pytest
from services.product_services import ProductService, ProductModel

# Example connection string for local MongoDB server
connection_string = "mongodb://localhost:27017/"


@pytest.fixture
def product_service():
    return ProductService()


# Parametrized tests for the ProductService class in product_service.py

# Test adding a product using the ProductService class
@pytest.mark.parametrize("product_data",
                         [ProductModel(name="TestProduct", price=19.99, discount=5, category="TestCategory"),
                          ProductModel(name="TestProductEdge1", price=19.99, discount=5, category="TestCategory"),
                          ProductModel(name="TestProductEdge2", price=19.99, discount=5, category="TestCategory")])
def test_add_product(product_service, product_data):
    result = product_service.add_product(product_data)
    assert "oid" in result


# Test getting a product using the ProductService class
@pytest.mark.parametrize("product_data",
                         [ProductModel(name="TestProduct", price=19.99, discount=5, category="TestCategory"),
                          ProductModel(name="TestProductEdge1", price=19.99, discount=5, category="TestCategory"),
                          ProductModel(name="TestProductEdge2", price=19.99, discount=5, category="TestCategory")])
def test_get_product(product_service, product_data):
    result = product_service.get_product(product_data)
    assert result is not None


# Test updating a product using the ProductService class
@pytest.mark.parametrize("product_data",
                         [ProductModel(name="TestProduct", price=29.99, discount=10, category="TestCategory"),
                          ProductModel(name="TestProductEdge1", price=29.99, discount=10, category="TestCategory"),
                          ProductModel(name="TestProductEdge2", price=29.99, discount=10, category="TestCategory")])
def test_update_product(product_service, product_data):
    result = product_service.update_product(product_data)
    assert "message" in result


# Test deleting a product using the ProductService class
@pytest.mark.parametrize("product_data",
                         [ProductModel(name="TestProduct", price=29.99, discount=10, category="TestCategory"),
                          ProductModel(name="TestProductEdge1", price=29.99, discount=10, category="TestCategory"),
                          ProductModel(name="TestProductEdge2", price=29.99, discount=10, category="TestCategory")])
def test_delete_product(product_service, product_data):
    result = product_service.delete_product(product_data)
    assert "message" in result


# Test getting products using the ProductService class
@pytest.mark.parametrize("products_data",
                         [[ProductModel(name="TestProduct", price=19.99, discount=5, category="TestCategory")],
                          [ProductModel(name="TestProductEdge1", price=19.99, discount=5, category="TestCategory")],
                          [ProductModel(name="TestProductEdge2", price=19.99, discount=5, category="TestCategory")]])
def test_get_products(product_service, products_data):
    result = product_service.get_products(products_data)
    assert isinstance(result, list)

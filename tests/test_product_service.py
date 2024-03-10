import os
import pytest

from services.product_services import ProductService
from model.product_model import ProductModel


@pytest.fixture(scope="module")
def product_service():
    # Assuming your config.json is in the parent directory
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
    service = ProductService(config_path)

    # Initialize the database for testing
    db_name = "test_db"
    collection_name = "test_collection"
    service.db_name = db_name
    service.collection_name = collection_name
    return service


def test_add_product(product_service):
    # Test adding a product
    # Clear the test collection
    product_service.db_store.client["test_db"]["test_collection"].delete_many({})

    product_data = ProductModel(name="TestProduct", price=19.99, discount=5, category="TestCategory")
    result = product_service.add_product(product_data)
    result_2 = product_service.get_product_by_name(product_data.name)
    print(result)
    print(result_2)

    assert result is not None
    assert str(result_2.get("_id")) == result.get("oid")
    assert result_2.get("name") == product_data.name
    assert result_2.get("price") == product_data.price
    assert result_2.get("discount") == product_data.discount
    assert result_2.get("category") == product_data.category
    print(result)


def test_get_all_products(product_service):
    product_service.db_store.client["test_db"]["test_collection"].delete_many({})
    # Test getting all products
    result = product_service.get_all_products()
    assert isinstance(result, list)
    assert len(result) == 0
    products_data = [ProductModel(name="TestProduct1", price=19.99, discount=5, category="TestCategory1"),
                     ProductModel(name="TestProduct2", price=10.4, discount=2, category="TestCategory2"),
                     ProductModel(name="TestProduct3", price=5.3, discount=1, category="TestCategory3")]
    i = 1
    for product_data in products_data:
        result = product_service.add_product(product_data)
        result_2 = product_service.get_all_products()
        print(result_2)
        assert len(result_2) == i
        i += 1
        assert result_2[-1]["name"] == product_data.name

    print(result)


def test_update_product(product_service):
    # Test updating a product
    # Clear the test collection
    product_service.db_store.client["test_db"]["test_collection"].delete_many({})

    # Add a product for updating
    product_data = ProductModel(name="TestProduct", price=19.99, discount=5, category="TestCategory")
    product_service.add_product(product_data)

    # Get the product before update
    product_before_update = product_service.get_product_by_name(product_data.name)

    # Update the product data
    updated_product_data = {
        "reference_name": product_data.name,
        "name": "UpdatedTestProduct",
        "price": 29.99,
        "discount": 10,
        "category": "UpdatedTestCategory"
    }

    product_service.update_product(updated_product_data)

    # Get the product after update
    product_after_update = product_service.get_product_by_name(updated_product_data["name"])

    # Assertions

    assert product_before_update.get("name") == product_data.name
    assert product_after_update.get("name") == updated_product_data["name"]
    assert product_after_update.get("price") == updated_product_data["price"]
    assert product_after_update.get("discount") == updated_product_data["discount"]
    assert product_after_update.get("category") == updated_product_data["category"]


def test_delete_product(product_service):
    # Test deleting a product
    # Clear the test collection
    product_service.db_store.client["test_db"]["test_collection"].delete_many({})

    # Add a product for deletion
    product_data = ProductModel(name="TestProduct", price=19.99, discount=5, category="TestCategory")
    product_service.add_product(product_data)

    # Get the product before deletion
    product_before_deletion = product_service.get_product_by_name(product_data.name)

    # Delete the product
    result = product_service.delete_product(product_data.name)
    assert result is True

    # Get the product after deletion
    product_after_deletion = product_service.get_product_by_name(product_data.name)

    # Assertions
    assert product_before_deletion is not None
    assert product_after_deletion is None

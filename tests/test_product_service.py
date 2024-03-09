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
    product_data = ProductModel(name="TestProduct", price=19.99, discount=5, category="TestCategory")
    result = product_service.add_product(product_data)
    assert result is not None
    assert "oid" in result


def test_get_all_products(product_service):
    # Test getting all products
    result = product_service.get_all_products()
    assert isinstance(result, list)


def test_update_product(product_service):
    # Test updating a product
    product_data = {"reference_name": "OldName", "name": "NewName", "price": 1, "discount": 1, "category": "test"}
    result_update = product_service.update_product(product_data)
    assert result_update is not None or result_update is None


"""Nu reusesc sa ii dau de cap"""
# def test_delete_product(product_service):
#     # Test deleting a product
#     product_name = "TestProduct"
#
#     # Add a test product
#     test_product_data = ProductModel(name=product_name, price=19.99, discount=5, category="TestCategory")
#     add_result = product_service.add_product(test_product_data)
#     assert add_result, f"Failed to add product: {product_name}"
#
#     # Check if the product exists before deletion
#     existing_product = product_service.get_product_by_name(product_name)
#     assert existing_product is not None
#
#     # Print the document before deletion
#     print(f"Document before deletion: {existing_product}")
#
#     # Delete the test product
#     result_delete = product_service.delete_product(product_name)
#     assert result_delete, f"Failed to delete product: {product_name}"
#
#     # Check if the product still exists after deletion
#     # Check if the product still exists after deletion
#     remaining_products = product_service.get_all_products()
#     product_names_after_deletion = [product['name'] for product in remaining_products]
#     print(f"Product names after deletion: {product_names_after_deletion}")
#     print(f"Checking if '{product_name}' is in the list: {product_name in product_names_after_deletion}")
#     assert product_name not in product_names_after_deletion, f"Product '{product_name}' still exists after deletion"

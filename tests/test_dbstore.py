import pytest
from utils.dbstore import DBStore


@pytest.fixture
def test_data():
    data = {
        "predefined_payload": {
            "name": "TestProduct",
            "price": 19.99,
            "discount": 5,
            "category": "TestCategory"
        },
        "db_store": DBStore('mongodb://localhost:27017/'),
        "test_db_name": 'test_db',
        "test_collection_name": 'test_collection'
    }
    return data


"""Nu reusesc sa ii dau de cap"""


# def test_initialize_database(test_data):
#     # Arrange
#     db_store = test_data["db_store"]
#     test_db_name = test_data["test_db_name"]
#     test_collection_name = test_data["test_collection_name"]
#
#     # Act
#     result = db_store.initialize_database(test_db_name, test_collection_name)
#
#     # Assert
#     assert result is not None
#     assert result["name"] == "TestProduct"
#     assert result["price"] == 19.99
#     assert result["discount"] == 5
#     assert result["category"] == "TestCategory"
#
#     # Clean up: Delete the test document from the collection
#     db_store.delete_document_by_name(test_db_name, test_collection_name, "TestProduct")


def test_add_document(test_data):
    predefined_payload = test_data["predefined_payload"]
    db_store = test_data["db_store"]
    test_db_name = test_data["test_db_name"]
    test_collection_name = test_data["test_collection_name"]

    # Test adding a document
    result = db_store.add_document(test_db_name, test_collection_name, predefined_payload)

    assert result.get("oid") is not None


def test_find_document_by_key(test_data):
    predefined_payload = test_data["predefined_payload"]
    db_store = test_data["db_store"]
    test_db_name = test_data["test_db_name"]
    test_collection_name = test_data["test_collection_name"]

    # Add a document before testing find_document_by_key
    db_store.add_document(test_db_name, test_collection_name, predefined_payload)

    # Test finding the document by key
    result = db_store.find_document_by_key(test_db_name, test_collection_name, "_id", predefined_payload["_id"])
    assert result == predefined_payload


def test_find_documents_by_key(test_data):
    # Arrange
    db_store = test_data["db_store"]
    test_db_name = test_data["test_db_name"]
    test_collection_name = test_data["test_collection_name"]

    # Clear the test collection
    db_store.client[test_db_name][test_collection_name].delete_many({})

    # Add a test document to the collection
    test_payload = test_data["predefined_payload"]
    db_store.add_document(test_db_name, test_collection_name, test_payload)

    # Act
    result = db_store.find_documents_by_key(test_db_name, test_collection_name, "name", "TestProduct")

    # Assert
    assert len(result) == 1


def test_update_document_by_name(test_data):
    db_store = test_data["db_store"]
    test_db_name = test_data["test_db_name"]
    test_collection_name = test_data["test_collection_name"]
    predefined_payload = test_data["predefined_payload"]

    # Add a document before testing update_document_by_name
    db_store.add_document(test_db_name, test_collection_name, predefined_payload)

    # Update the document
    update_payload = {"price": 29.99, "discount": 10}
    updated_document = db_store.update_document_by_name(test_db_name, test_collection_name, "TestProduct",
                                                        update_payload)

    assert updated_document is not None
    assert updated_document['price'] == update_payload['price']
    assert updated_document['discount'] == update_payload['discount']


def test_delete_document_by_name(test_data):
    db_store = test_data["db_store"]
    test_db_name = test_data["test_db_name"]
    test_collection_name = test_data["test_collection_name"]
    predefined_payload = test_data["predefined_payload"]

    # Add a document before testing delete_document_by_name
    db_store.add_document(test_db_name, test_collection_name, predefined_payload)

    # Delete the document
    result = db_store.delete_document_by_name(test_db_name, test_collection_name, "TestProduct")

    assert result is True  # Document should be deleted

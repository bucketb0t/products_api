import pytest
from utils.dbstore import DBStore

# Example connection string for local MongoDB server
connection_string = "mongodb://localhost:27017/"


@pytest.fixture
def db_store():
    return DBStore(connection_string)


# Parametrized tests for the DBStore class in dbstore.py

# Test initialization of the database with a test document
@pytest.mark.parametrize("db_name, collection_name",
                         [("test_db", "test_collection"), ("test_db", "test_collection_edge1"),
                          ("test_db_edge2", "test_collection")])
def test_initialize_database(db_store, db_name, collection_name):
    result = db_store.initialize_database(db_name, collection_name)
    assert result is not None


# Test adding a document to the database
@pytest.mark.parametrize("db_name, collection_name, payload", [
    ("test_db", "test_collection", {"name": "TestProduct", "price": 19.99, "discount": 5, "category": "TestCategory"}),
    ("test_db", "test_collection_edge1",
     {"name": "TestProduct", "price": 19.99, "discount": 5, "category": "TestCategory"}), (
    "test_db_edge2", "test_collection",
    {"name": "TestProduct", "price": 19.99, "discount": 5, "category": "TestCategory"})])
def test_add_document(db_store, db_name, collection_name, payload):
    result = db_store.add_document(db_name, collection_name, payload)
    assert "oid" in result


# Test finding a document by key in the database
@pytest.mark.parametrize("db_name, collection_name, key",
                         [("test_db", "test_collection", "name"), ("test_db", "test_collection_edge1", "name"),
                          ("test_db_edge2", "test_collection", "name")])
def test_find_document_by_key(db_store, db_name, collection_name, key):
    result = db_store.find_document_by_key(db_name, collection_name, key)
    assert result is not None


# Test finding documents by key in the database
@pytest.mark.parametrize("db_name, collection_name, key",
                         [("test_db", "test_collection", "name"), ("test_db", "test_collection_edge1", "name"),
                          ("test_db_edge2", "test_collection", "name")])
def test_find_documents_by_key(db_store, db_name, collection_name, key):
    result = db_store.find_documents_by_key(db_name, collection_name, key)
    assert isinstance(result, list)


# Test updating a document by name in the database
@pytest.mark.parametrize("db_name, collection_name, name, payload",
                         [("test_db", "test_collection", "TestProduct", {"price": 29.99}),
                          ("test_db", "test_collection_edge1", "TestProduct", {"price": 29.99}),
                          ("test_db_edge2", "test_collection", "TestProduct", {"price": 29.99})])
def test_update_document_by_name(db_store, db_name, collection_name, name, payload):
    result = db_store.update_document_by_name(db_name, collection_name, name, payload)
    assert "message" in result


# Test deleting a document by name in the database
@pytest.mark.parametrize("db_name, collection_name, name", [("test_db", "test_collection", "TestProduct"),
                                                            ("test_db", "test_collection_edge1", "TestProduct"),
                                                            ("test_db_edge2", "test_collection", "TestProduct")])
def test_delete_document_by_name(db_store, db_name, collection_name, name):
    result = db_store.delete_document_by_name(db_name, collection_name, name)
    assert "message" in result

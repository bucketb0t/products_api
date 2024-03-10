from pymongo import MongoClient
from bson import ObjectId


class DBStore:
    def __init__(self, connection_string):
        # Initialize a MongoDB client with the provided connection string
        self.client = MongoClient(connection_string)

    def initialize_database(self, db_name, collection_name):
        """
        Initialize the database by adding a test document, retrieving it, and then deleting it.
        :param db_name: Name of the MongoDB database
        :param collection_name: Name of the MongoDB collection
        :return: The test document added and deleted
        """
        test_payload = {
            "name": "TestProduct",
            "price": 19.99,
            "discount": 5,
            "category": "TestCategory"
        }

        # Add a test document
        test_result = self.add_document(db_name, collection_name, test_payload)
        test_oid = test_result.get("oid")

        # Retrieve the test document
        test_document = self.find_document_by_key(db_name, collection_name, "_id", ObjectId(test_oid))

        # Delete the test document
        if test_oid:
            self.delete_document_by_name(db_name, collection_name, test_payload["name"])

        return test_document

    def add_document(self, db_name, collection_name, payload):
        """
        Add a document to the specified MongoDB database and collection.
        :param db_name: Name of the MongoDB database
        :param collection_name: Name of the MongoDB collection
        :param payload: Document data to be added
        :return: Dictionary containing the ObjectId of the added document
        """
        db = self.client[db_name]
        collection = db[collection_name]
        result = collection.insert_one(payload)
        print(f"Document added oid {str(result.inserted_id)}")
        return {"oid": str(result.inserted_id)}

    def find_document_by_key(self, db_name, collection_name, key, value):
        """
        Find a document in the specified MongoDB database and collection by a key.
        :param db_name: Name of the MongoDB database
        :param collection_name: Name of the MongoDB collection
        :param key: Key to search for in the document
        :param value: Value corresponding to the key
        :return: The found document or None if not found
        """
        db = self.client[db_name]
        collection = db[collection_name]
        document = collection.find_one({key: value})
        print(f"Document found! {document}")
        return document

    def find_documents_by_key(self, db_name, collection_name, key=None, value=None):
        """
        Find documents in the specified MongoDB database and collection by a key.
        :param db_name: Name of the MongoDB database
        :param collection_name: Name of the MongoDB collection
        :param key: Key to search for in the documents
        :return: List of found documents or an empty list if none found
        """
        db = self.client[db_name]
        collection = db[collection_name]
        if key is None or value is None:
            documents = list(collection.find())  # echivalentul al get all products
        else:
            documents = list(collection.find({key: value}))  # echivalentul pe get all product cu numele xulescu
        print(f"Documents found: {documents}")
        return documents

    def update_document_by_name(self, db_name, collection_name, name, payload):
        """
        Update a document in the specified MongoDB database and collection by name.
        :param db_name: Name of the MongoDB database
        :param collection_name: Name of the MongoDB collection
        :param name: Name field in the document to be updated
        :param payload: New data to update in the document
        :return: Dictionary containing a message about the update status
        """
        db = self.client[db_name]
        collection = db[collection_name]
        print(f"Querry: {name} // {payload}")
        result = collection.update_one({"name": name}, {"$set": payload})

        updated_document = collection.find_one(payload)

        if result.modified_count == 1:
            print(f"Document updated! {payload}")
        else:
            print(f"Document failed to update! {payload}")

        return updated_document

    def delete_document_by_name(self, db_name, collection_name, name):
        """
        Delete a document in the specified MongoDB database and collection by name.
        :param db_name: Name of the MongoDB database
        :param collection_name: Name of the MongoDB collection
        :param name: Name field in the document to be deleted
        :return: Dictionary containing a message about the delete status
        """
        db = self.client[db_name]
        collection = db[collection_name]
        result = collection.delete_one({"name": name})

        if result.deleted_count > 0:
            print(f"Document deleted! {name}")
            return True
        else:
            print(f"Document failed to be deleted! {name}")
            return False

import json
from utils.dbstore import DBStore
from pydantic import BaseModel
from typing import List



class ProductModel(BaseModel):
    """
    Reuse the ProductModel from product_model.py.
    """
    name: str
    price: float
    discount: int
    category: str


class ProductService:
    def __init__(self, config_path='D:/Seby_Python/python_projects/products_api/config.json'):
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)

        # Extract data_dir and port from the configuration
        data_dir = config_data.get('data_dir')
        port = config_data.get('port')

        # Construct the MongoDB connection string
        connection_string = f"mongodb://localhost:{port}/"
        self.db_store = DBStore(connection_string)

        # Set fixed database and collection names
        self.db_name = "schema_project"
        self.collection_name = "schema_project_collection"

    def add_product(self, product_data: ProductModel):
        """
        Add a product using the DBStore add_document method.
        :param product_data: Product data to be added
        :return: Dictionary containing the ObjectId of the added document
        """
        payload = product_data.dict()
        result = self.db_store.add_document(self.db_name, self.collection_name, payload)
        return result

    def get_product(self, product_data: ProductModel):
        """
        Get a product using the DBStore find_document_by_key method.
        :param product_data: Product data to be used for finding the document
        :return: The found document or None if not found
        """
        key = "name"
        result = self.db_store.find_document_by_key(self.db_name, self.collection_name, key)
        return result

    def update_product(self, product_data: ProductModel):
        """
        Update a product using the DBStore update_document_by_name method.
        :param product_data: Product data for updating the document
        :return: Dictionary containing a message about the update status
        """
        name = product_data.name
        payload = product_data.dict()
        result = self.db_store.update_document_by_name(self.db_name, self.collection_name, name, payload)
        return result

    def delete_product(self, product_data: ProductModel):
        """
        Delete a product using the DBStore delete_document_by_name method.
        :param product_data: Product data for deleting the document
        :return: Dictionary containing a message about the delete status
        """
        name = product_data.name
        result = self.db_store.delete_document_by_name(self.db_name, self.collection_name, name)
        return result

    def get_products(self, products_data: List[ProductModel]) -> List[dict]:
        """
        Get a list of products using the DBStore find_documents_by_key method.
        :param products_data: List of product data to be used for finding the documents
        :return: List of found documents or an empty list if none found
        """
        key = "name"
        result = self.db_store.find_documents_by_key(self.db_name, self.collection_name, key)
        return result

# Example usage:
# product_service = ProductService()
# product_data = ProductModel(name="TestProduct", price=19.99, discount=5, category="TestCategory")
# result = product_service.add_product(product_data)
# print(result)
# (Similarly, you can use other methods like get_product, update_product, delete_product, get_products)

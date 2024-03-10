import os
import json
from typing import List

from utils.dbstore import DBStore
from model.product_model import ProductModel


class ProductService:
    def __init__(self, config_path=None):
        if config_path is None:
            # Get the directory path of the current module
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Navigate to the parent directory and then to the config file
            config_path = os.path.join(current_dir, '..', 'config.json')

        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)

        # Extract data_dir and port from the configuration
        config_data.get('data_dir')
        port = config_data.get('port')

        # Construct the MongoDB connection string
        connection_string = f"mongodb://localhost:{port}/"
        self.db_store = DBStore(connection_string)

        # Set fixed database and collection names
        self.db_name = "products"
        self.collection_name = "products"
        # find waldo

    def add_product(self, product_data: ProductModel):
        """
        Add a product using the DBStore add_document method.
        :param product_data: Product data to be added
        :return: Dictionary containing the ObjectId of the added document
        """
        payload = product_data.dict()
        result = self.db_store.add_document(self.db_name, self.collection_name, payload)
        return result

    def get_product_by_name(self, name_of_product: str):
        """
        Get a product using the DBStore find_document_by_key method
        :return: The found document or None if not found
        """
        result = self.db_store.find_document_by_key(self.db_name, self.collection_name, key="name",
                                                    value=name_of_product)
        return result

    def get_all_products(self) -> List[dict]:
        """
        Get a list of products using the DBStore find_documents_by_key method.
        :return: List of found documents or an empty list if none found
        """
        result = self.db_store.find_documents_by_key(self.db_name, self.collection_name)
        return result

    def update_product(self, product_data: dict):
        """
        Update a product using the DBStore update_document_by_name method.
        :param product_data: Product data for updating the document plus a key value pair with old name of the product
        :return: Dictionary containing a message about the update status
        """
        reference_name = product_data.get("reference_name")
        del product_data["reference_name"]
        payload = product_data
        result = self.db_store.update_document_by_name(self.db_name, self.collection_name, reference_name, payload)

        return result

    def delete_product(self, name_of_product: str):
        """
        Delete a product using the DBStore delete_document_by_name method.
        :param name_of_product: Product data for deleting the document
        :return: Dictionary containing a message about the delete status
        """
        # Print the products before deletion
        all_products_before_deletion = self.get_all_products()
        print(f"All products before deletion: {all_products_before_deletion}")

        # Delete the product
        result = self.db_store.delete_document_by_name(self.db_name, self.collection_name, name_of_product)

        # Print the products after deletion
        all_products_after_deletion = self.get_all_products()
        print(f"All products after deletion: {all_products_after_deletion}")

        return result

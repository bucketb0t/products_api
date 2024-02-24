from pydantic import BaseModel

class ProductModel(BaseModel):
    """
    Pydantic model representing a product with specific fields and their types.
    """
    name: str
    price: float
    discount: int
    category: str

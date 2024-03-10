from fastapi import APIRouter, HTTPException
from typing import List

from model.product_model import ProductModel
from services.product_services import ProductService

router = APIRouter()
product_service = ProductService()


@router.post("/", response_model=dict)
async def create_product(product_data: ProductModel):
    return product_service.add_product(product_data)


@router.get("/{name}", response_model=ProductModel)
async def read_product(name: str):
    result = product_service.get_product_by_name(name)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found!")
    return result


@router.get("/", response_model=List[ProductModel])
async def read_products():
    return product_service.get_all_products()


@router.put("/{name}", response_model=ProductModel)
async def update_product(name: str, product_data: ProductModel):
    payload = {
        "reference_name": name,
        "name": product_data.name,
        "price": product_data.price,
        "discount": product_data.discount,
        "category": product_data.category
    }

    return product_service.update_product(payload)


@router.delete("/{name}", response_model=bool)
async def delete_product(name: str):
    return product_service.delete_product(name)

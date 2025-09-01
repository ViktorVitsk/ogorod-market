from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from . import service, schemas

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[schemas.Product])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    products = await service.get_products(db, skip, limit)
    return products

@router.get("/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/by-slug/{slug}", response_model=schemas.Product)
async def read_product_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    product = await service.get_product_by_slug(db, slug)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_superuser

from . import schemas, service

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/', response_model=List[schemas.Product])
async def read_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    products = await service.get_products(db, skip, limit)
    return products


@router.get('/{product_id}', response_model=schemas.Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return product


@router.get('/by-slug/{slug}', response_model=schemas.Product)
async def read_product_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    product = await service.get_product_by_slug(db, slug)
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return product


@router.post('/', response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: schemas.ProductCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_superuser),
):
    product = await service.create_product(db, product_in)
    return product


@router.patch('/{product_id}', response_model=schemas.Product)
async def update_product(
    product_id: int,
    product_in: schemas.ProductUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_superuser),
):
    product = await service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    updated = await service.update_product(db, product, product_in)
    return updated


@router.delete(
    '/{product_id}', response_model=schemas.Product, status_code=status.HTTP_200_OK
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_superuser),
):
    product = await service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    deactivated = await service.deactivate_product(db, product)
    return deactivated

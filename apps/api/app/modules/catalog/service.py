from unittest import result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Product

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Product)
        .where(Product.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
        .where(Product.is_active == True)
    )
    return result.scalar_one_or_none()

async def get_product_by_slug(db: AsyncSession, slug: str):
    result = await db.execute(
        select(Product)
        .where(Product.slug == slug)
        .where(Product.is_active == True)
    )
    return result.scalar_one_or_none()
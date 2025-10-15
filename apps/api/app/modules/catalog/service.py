from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product
from .schemas import ProductCreate, ProductUpdate


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Product).where(Product.is_active).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(Product).where(Product.id == product_id).where(Product.is_active)
    )
    return result.scalar_one_or_none()


async def get_product_by_slug(db: AsyncSession, slug: str):
    result = await db.execute(
        select(Product).where(Product.slug == slug).where(Product.is_active)
    )
    return result.scalar_one_or_none()


async def create_product(db: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update_product(
    db: AsyncSession, product: Product, product_in: ProductUpdate
) -> Product:
    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    return product


async def deactivate_product(db: AsyncSession, product: Product) -> Product:
    product.is_active = False
    await db.commit()
    await db.refresh(product)
    return product

from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.catalog.models import Product

from .models import Cart, CartItem


def _cart_query(user_id: int):
    return (
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(selectinload(Cart.items))
    )


async def get_cart(db: AsyncSession, user_id: int) -> Cart | None:
    result = await db.execute(
        _cart_query(user_id).execution_options(populate_existing=True)
    )
    return result.scalar_one_or_none()


async def get_or_create_cart(db: AsyncSession, user_id: int) -> Cart:
    cart = await get_cart(db, user_id)
    if cart is not None:
        return cart

    db.add(Cart(user_id=user_id))
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        existing = await get_cart(db, user_id)
        if existing is None:
            raise
        return existing

    created = await get_cart(db, user_id)
    if created is None:
        raise RuntimeError('Cart disappeared after insert')
    return created


async def _get_active_product(db: AsyncSession, product_id: int) -> Product:
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.is_active.is_(True))
    )
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found',
        )
    return product


async def _reload_cart(db: AsyncSession, user_id: int) -> Cart:
    cart = await get_cart(db, user_id)
    if cart is None:
        raise RuntimeError('Cart disappeared after update')
    return cart


async def add_or_update_item(
    db: AsyncSession,
    cart: Cart,
    product_id: int,
    quantity: int,
) -> Cart:
    product = await _get_active_product(db, product_id)
    result = await db.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id,
        )
    )
    item = result.scalar_one_or_none()
    if item is None:
        db.add(
            CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                price=Decimal(product.price),
            )
        )
    else:
        item.quantity = quantity

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Cart item already exists',
        ) from None
    return await _reload_cart(db, cart.user_id)


async def update_item_quantity(
    db: AsyncSession,
    cart: Cart,
    item_id: int,
    quantity: int,
) -> Cart:
    result = await db.execute(
        select(CartItem).where(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id,
        )
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Cart item not found',
        )
    item.quantity = quantity
    await db.commit()
    return await _reload_cart(db, cart.user_id)


async def remove_item(db: AsyncSession, cart: Cart, item_id: int) -> Cart:
    result = await db.execute(
        select(CartItem).where(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id,
        )
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Cart item not found',
        )
    await db.delete(item)
    await db.commit()
    return await _reload_cart(db, cart.user_id)

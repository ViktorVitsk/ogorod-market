from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models import Product

from .models import Cart, CartItem
from .schemas import CartItemCreate


async def get_or_create_cart(db: AsyncSession, user_id: int) -> Cart:
    result = await db.execute(select(Cart).where(Cart.user_id == user_id))
    cart = result.scalar_one_or_none()
    if cart:
        return cart

    cart = Cart(user_id=user_id)
    db.add(cart)
    await db.commit()
    await db.refresh(cart)
    return cart


async def get_cart(db: AsyncSession, user_id: int) -> Optional[Cart]:
    result = await db.execute(select(Cart).where(Cart.user_id == user_id).options())
    return result.scalar_one_or_none()


async def add_or_update_item(
    db: AsyncSession,
    cart: Cart,
    item_data: CartItemCreate,
) -> Cart:
    result = await db.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == item_data.product_id,
        )
    )
    item = result.scalar_one_or_none()

    if item:
        item.quantity = item_data.quantity
        item.price = item_data.price
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            price=item_data.price,
        )
        db.add(item)

    await db.commit()
    await db.refresh(cart)
    return cart


async def remove_item(db: AsyncSession, cart: Cart, item_id: int) -> Cart:
    result = await db.execute(
        select(CartItem).where(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id,
        )
    )
    item = result.scalar_one_or_none()
    if item:
        await db.delete(item)
        await db.commit()
    await db.refresh(cart)
    return cart


async def calculate_price(db: AsyncSession, product_id: int) -> Decimal:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise ValueError('Product not found')
    return Decimal(product.price)

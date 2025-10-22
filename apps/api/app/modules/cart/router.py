from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User

from . import schemas, service

router = APIRouter(prefix='/cart', tags=['cart'])


@router.get('/', response_model=schemas.CartRead)
async def read_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cart = await service.get_cart(db, current_user.id)
    return cart


@router.post('/items', response_model=schemas.CartRead, status_code=status.HTTP_200_OK)
async def add_item(
    item_in: schemas.CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cart = await service.get_or_create_cart(db, current_user.id)
    cart = await service.add_or_update_item(db, cart, item_in)
    return cart


@router.patch('/items/{item_id}', response_model=schemas.CartRead)
async def update_item(
    item_id: int,
    item_in: schemas.CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cart = await service.get_or_create_cart(db, current_user.id)
    item = await service.add_or_update_item(  # обновим количество
        db,
        cart,
        schemas.CartItemCreate(
            product_id=item_id,  # см. примечание ниже
            quantity=item_in.quantity,
            price=await service.calculate_price(db, item_id),
        ),
    )
    return item


@router.delete('/items/{item_id}', response_model=schemas.CartRead)
async def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cart = await service.get_or_create_cart(db, current_user.id)
    cart = await service.remove_item(db, cart, item_id)
    return cart

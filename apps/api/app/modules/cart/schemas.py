from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, conint


class CartItemBase(BaseModel):
    product_id: int
    quantity: conint(ge=1) = 1


class CartItemCreate(CartItemBase):
    price: Decimal


class CartItemUpdate(BaseModel):
    quantity: conint(ge=1)


class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CartRead(BaseModel):
    id: int
    user_id: int
    items: List[CartItemRead]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

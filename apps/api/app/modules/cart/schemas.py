from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)


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

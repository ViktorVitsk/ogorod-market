from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    unit: str = 'кг'
    stock_quantity: int = Field(default=0, ge=0)
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_featured: bool = False


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    unit: Optional[str] = None
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_featured: Optional[bool] = None


class ProductInDB(ProductBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Для ответа API используем эту схему (без служебных полей)
class Product(ProductInDB):
    pass

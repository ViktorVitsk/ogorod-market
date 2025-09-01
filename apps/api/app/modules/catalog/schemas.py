from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    price: Decimal
    unit: str = "кг"
    stock_quantity: int = 0
    category_id: int | None = None
    image_url: str | None = None
    is_featured: bool = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductInDB(ProductBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Для ответа API используем эту схему (без служебных полей)
class Product(ProductInDB):
    pass
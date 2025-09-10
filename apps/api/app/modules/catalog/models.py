from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, text
from sqlalchemy.orm import declarative_base
from  datetime import datetime, timezone

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(20), default="кг", server_default="кг")
    stock_quantity = Column(Integer, default=0, server_default="0")
    category_id = Column(Integer)
    image_url = Column(String(500))
    is_featured = Column(Boolean, default=False, server_default="false")
    is_active = Column(Boolean, default=True, server_default="true")
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    
    def __repr__(self):
        return f"<Product {self.name}>"
import asyncio
from sqlalchemy import text
from app.core.database import engine
from app.modules.catalog.models import Product
from sqlalchemy.ext.asyncio import AsyncSession

async def seed_database():
    async with AsyncSession(engine) as session:
        # Проверяем, есть ли уже данные
        result = await session.execute(text("SELECT COUNT(*) FROM products"))
        count = result.scalar()
        
        if count > 0:
            print("Database already has data, skipping seeding")
            return

        # Тестовые товары
        test_products = [
            Product(
                name="Свежие огурцы",
                slug="fresh-cucumbers",
                description="Сочные хрустящие огурчики с грядки",
                price=150.50,
                unit="кг",
                stock_quantity=100,
                category_id=1,
                image_url="/images/cucumbers.jpg"
            ),
            Product(
                name="Помидоры черри",
                slug="cherry-tomatoes", 
                description="Сладкие помидорки черри",
                price=200.00,
                unit="кг",
                stock_quantity=50,
                category_id=1,
                image_url="/images/tomatoes.jpg"
            ),
            Product(
                name="Морковь свежая",
                slug="fresh-carrots",
                description="Сладкая молодая морковь",
                price=80.00,
                unit="кг",
                stock_quantity=75,
                category_id=2,
                image_url="/images/carrots.jpg"
            )
        ]

        session.add_all(test_products)
        await session.commit()
        print(f"Added {len(test_products)} test products")

if __name__ == "__main__":
    asyncio.run(seed_database())
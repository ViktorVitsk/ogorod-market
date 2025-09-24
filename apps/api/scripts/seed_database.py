import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.modules.catalog.models import Product

async def seed_products():
    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже товары
        result = await session.execute(select(Product))
        existing_products = result.scalars().all()
        
        if existing_products:
            print(f"В базе уже есть {len(existing_products)} товаров. Пропускаем наполнение.")
            return

        # Тестовые овощи
        test_products = [
            Product(
                name="Свежие огурцы",
                slug="fresh-cucumbers",
                description="Сочные хрустящие огурчики прямо с грядки. Идеально для салатов и закусок.",
                price=150.50,
                unit="кг",
                stock_quantity=100,
                category_id=1,
                image_url="/images/cucumbers.jpg",
                is_featured=True
            ),
            Product(
                name="Помидоры черри",
                slug="cherry-tomatoes",
                description="Сладкие помидорки черри. Отлично подходят для салатов и украшения блюд.",
                price=200.00,
                unit="кг", 
                stock_quantity=50,
                category_id=1,
                image_url="/images/tomatoes.jpg",
                is_featured=True
            ),
            Product(
                name="Морковь свежая",
                slug="fresh-carrots", 
                description="Сладкая молодая морковь. Богата витаминами, идеальна для соков и салатов.",
                price=80.00,
                unit="кг",
                stock_quantity=75,
                category_id=2,
                image_url="/images/carrots.jpg"
            ),
            Product(
                name="Картофель молодой",
                slug="young-potatoes",
                description="Молодой картофель с нежной кожицей. Вкусен в вареном и запеченном виде.",
                price=60.00,
                unit="кг",
                stock_quantity=200,
                category_id=2,
                image_url="/images/potatoes.jpg"
            ),
            Product(
                name="Капуста белокочанная",
                slug="white-cabbage",
                description="Свежая хрустящая капуста. Отлично для салатов, супов и тушения.",
                price=45.00, 
                unit="кг",
                stock_quantity=80,
                category_id=3,
                image_url="/images/cabbage.jpg"
            )
        ]

        session.add_all(test_products)
        await session.commit()
        print(f"✅ Добавлено {len(test_products)} тестовых товаров!")

        # Показываем что добавили
        result = await session.execute(select(Product))
        products = result.scalars().all()
        for product in products:
            print(f"  - {product.name}: {product.price} руб/{product.unit}")

if __name__ == "__main__":
    asyncio.run(seed_products())
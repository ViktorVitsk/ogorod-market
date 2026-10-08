import asyncio
from collections.abc import Awaitable, Callable

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.modules.auth.models import User
from app.modules.cart.models import Cart, CartItem
from app.modules.catalog.models import Product

_ = (User, Product, Cart, CartItem)


class ApiHarness:
    def __init__(self, client: AsyncClient, session_factory, engine):
        self.client = client
        self.session_factory = session_factory
        self.engine = engine

    @classmethod
    async def open(cls) -> 'ApiHarness':
        engine = create_async_engine(
            'sqlite+aiosqlite://',
            poolclass=StaticPool,
            connect_args={'check_same_thread': False},
        )
        session_factory = async_sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        async def override_get_db():
            async with session_factory() as session:
                yield session

        app.dependency_overrides[get_db] = override_get_db
        client = AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test',
        )
        return cls(client, session_factory, engine)

    async def close(self) -> None:
        await self.client.aclose()
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
        await self.engine.dispose()
        app.dependency_overrides.clear()


def async_api(fn: Callable[[ApiHarness], Awaitable[None]]):
    def wrapper():
        async def scenario():
            harness = await ApiHarness.open()
            try:
                await fn(harness)
            finally:
                await harness.close()

        asyncio.run(scenario())

    wrapper.__name__ = fn.__name__
    return wrapper


async def register_and_login(
    client: AsyncClient,
    email: str = 'user@example.com',
    password: str = 'password123',
    full_name: str = 'Test User',
) -> dict[str, str]:
    created = await client.post(
        '/api/auth/register',
        json={'email': email, 'password': password, 'full_name': full_name},
    )
    assert created.status_code == 201, created.text
    logged_in = await client.post(
        '/api/auth/login',
        json={'email': email, 'password': password},
    )
    assert logged_in.status_code == 200, logged_in.text
    return {'Authorization': f"Bearer {logged_in.json()['access_token']}"}


async def create_product(
    client: AsyncClient,
    *,
    name: str = 'Cucumber',
    slug: str = 'cucumber',
    price: float = 10.5,
) -> dict:
    response = await client.post(
        '/api/products/',
        json={
            'name': name,
            'slug': slug,
            'price': price,
            'stock_quantity': 5,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()

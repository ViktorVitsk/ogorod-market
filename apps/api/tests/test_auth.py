from sqlalchemy import select

from app.modules.auth.models import User
from tests.api import ApiHarness, async_api, register_and_login


@async_api
async def test_register_login_and_me(api: ApiHarness):
    created = await api.client.post(
        '/api/auth/register',
        json={
            'email': 'gardener@example.com',
            'password': 'password123',
            'full_name': 'Gardener',
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body['email'] == 'gardener@example.com'
    assert body['is_active'] is True
    assert 'password' not in body
    assert 'hashed_password' not in body

    logged_in = await api.client.post(
        '/api/auth/login',
        json={'email': 'gardener@example.com', 'password': 'password123'},
    )
    assert logged_in.status_code == 200
    token = logged_in.json()['access_token']
    assert logged_in.json()['token_type'] == 'bearer'

    me = await api.client.get(
        '/api/auth/me',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert me.status_code == 200
    assert me.json()['email'] == 'gardener@example.com'


@async_api
async def test_login_rejects_wrong_password(api: ApiHarness):
    await register_and_login(api.client)
    response = await api.client.post(
        '/api/auth/login',
        json={'email': 'user@example.com', 'password': 'wrong-password'},
    )
    assert response.status_code == 401


@async_api
async def test_duplicate_email_is_rejected(api: ApiHarness):
    await register_and_login(api.client)
    response = await api.client.post(
        '/api/auth/register',
        json={'email': 'user@example.com', 'password': 'password123'},
    )
    assert response.status_code == 400


@async_api
async def test_short_password_is_rejected(api: ApiHarness):
    response = await api.client.post(
        '/api/auth/register',
        json={'email': 'user@example.com', 'password': 'short'},
    )
    assert response.status_code == 422


@async_api
async def test_me_requires_a_valid_token(api: ApiHarness):
    missing = await api.client.get('/api/auth/me')
    assert missing.status_code == 401

    invalid = await api.client.get(
        '/api/auth/me',
        headers={'Authorization': 'Bearer not-a-token'},
    )
    assert invalid.status_code == 401


@async_api
async def test_inactive_user_cannot_login_or_reuse_a_token(api: ApiHarness):
    headers = await register_and_login(api.client)
    async with api.session_factory() as session:
        result = await session.execute(
            select(User).where(User.email == 'user@example.com')
        )
        user = result.scalar_one()
        user.is_active = False
        await session.commit()

    login = await api.client.post(
        '/api/auth/login',
        json={'email': 'user@example.com', 'password': 'password123'},
    )
    assert login.status_code == 401

    me = await api.client.get('/api/auth/me', headers=headers)
    assert me.status_code == 401

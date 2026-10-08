from tests.api import (
    ApiHarness,
    admin_headers,
    async_api,
    create_product,
    register_and_login,
)

PRODUCT = {'name': 'Dill', 'slug': 'dill', 'price': 3}


@async_api
async def test_health(api: ApiHarness):
    response = await api.client.get('/api/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


@async_api
async def test_product_can_be_created_and_read_by_slug(api: ApiHarness):
    catalog = await admin_headers(api)
    created = await create_product(api.client, headers=catalog, slug='fresh-cucumber')
    by_id = await api.client.get(f"/api/products/{created['id']}")
    by_slug = await api.client.get('/api/products/by-slug/fresh-cucumber')
    listing = await api.client.get('/api/products/')

    assert by_id.status_code == 200
    assert by_slug.status_code == 200
    assert by_slug.json()['name'] == 'Cucumber'
    assert any(item['slug'] == 'fresh-cucumber' for item in listing.json())


@async_api
async def test_duplicate_slug_is_rejected(api: ApiHarness):
    catalog = await admin_headers(api)
    await create_product(api.client, headers=catalog, slug='cucumber')
    response = await api.client.post(
        '/api/products/',
        headers=catalog,
        json={'name': 'Another', 'slug': 'cucumber', 'price': 12},
    )
    assert response.status_code == 409


@async_api
async def test_negative_price_and_oversized_page_are_rejected(api: ApiHarness):
    catalog = await admin_headers(api)
    negative = await api.client.post(
        '/api/products/',
        headers=catalog,
        json={'name': 'Bad', 'slug': 'bad', 'price': -1},
    )
    oversized = await api.client.get('/api/products/', params={'limit': 1000})
    assert negative.status_code == 422
    assert oversized.status_code == 422


@async_api
async def test_deactivated_product_is_hidden(api: ApiHarness):
    catalog = await admin_headers(api)
    created = await create_product(api.client, headers=catalog, slug='hidden-carrot')
    deleted = await api.client.delete(f"/api/products/{created['id']}", headers=catalog)
    assert deleted.status_code == 200
    assert deleted.json()['is_active'] is False

    listing = await api.client.get('/api/products/')
    by_id = await api.client.get(f"/api/products/{created['id']}")
    assert listing.json() == []
    assert by_id.status_code == 404
    assert by_id.json()['detail'] == 'Product not found'


@async_api
async def test_catalog_writes_are_limited_to_superusers(api: ApiHarness):
    anonymous_create = await api.client.post('/api/products/', json=PRODUCT)
    anonymous_update = await api.client.patch('/api/products/1', json={'name': 'Other'})
    anonymous_delete = await api.client.delete('/api/products/1')
    assert anonymous_create.status_code == 401
    assert anonymous_update.status_code == 401
    assert anonymous_delete.status_code == 401

    public_list = await api.client.get('/api/products/')
    assert public_list.status_code == 200

    customer = await register_and_login(api.client)
    forbidden_create = await api.client.post(
        '/api/products/', headers=customer, json=PRODUCT
    )
    forbidden_update = await api.client.patch(
        '/api/products/1', headers=customer, json={'price': 4}
    )
    forbidden_delete = await api.client.delete('/api/products/1', headers=customer)
    assert forbidden_create.status_code == 403
    assert forbidden_update.status_code == 403
    assert forbidden_delete.status_code == 403
    assert forbidden_create.json()['detail'] == 'Not enough permissions'

    owner = await admin_headers(api, email='owner@example.com')
    created = await create_product(api.client, headers=owner, slug='dill', name='Dill', price=3)
    updated = await api.client.patch(
        f"/api/products/{created['id']}",
        headers=owner,
        json={'price': 4},
    )
    assert updated.status_code == 200
    assert updated.json()['price'] == 4

    still_forbidden = await api.client.delete(
        f"/api/products/{created['id']}", headers=customer
    )
    assert still_forbidden.status_code == 403

    removed = await api.client.delete(f"/api/products/{created['id']}", headers=owner)
    assert removed.status_code == 200
    assert removed.json()['is_active'] is False


@async_api
async def test_registration_cannot_grant_superuser(api: ApiHarness):
    created = await api.client.post(
        '/api/auth/register',
        json={
            'email': 'aspiring-admin@example.com',
            'password': 'password123',
            'full_name': 'Aspiring',
            'is_superuser': True,
        },
    )
    assert created.status_code == 201
    assert created.json()['is_superuser'] is False

    logged_in = await api.client.post(
        '/api/auth/login',
        json={'email': 'aspiring-admin@example.com', 'password': 'password123'},
    )
    headers = {'Authorization': f"Bearer {logged_in.json()['access_token']}"}
    response = await api.client.post('/api/products/', headers=headers, json=PRODUCT)
    assert response.status_code == 403

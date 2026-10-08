from tests.api import ApiHarness, async_api, create_product


@async_api
async def test_health(api: ApiHarness):
    response = await api.client.get('/api/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


@async_api
async def test_product_can_be_created_and_read_by_slug(api: ApiHarness):
    created = await create_product(api.client, slug='fresh-cucumber')
    by_id = await api.client.get(f"/api/products/{created['id']}")
    by_slug = await api.client.get('/api/products/by-slug/fresh-cucumber')
    listing = await api.client.get('/api/products/')

    assert by_id.status_code == 200
    assert by_slug.status_code == 200
    assert by_slug.json()['name'] == 'Cucumber'
    assert any(item['slug'] == 'fresh-cucumber' for item in listing.json())


@async_api
async def test_duplicate_slug_is_rejected(api: ApiHarness):
    await create_product(api.client, slug='cucumber')
    response = await api.client.post(
        '/api/products/',
        json={'name': 'Another', 'slug': 'cucumber', 'price': 12},
    )
    assert response.status_code == 409


@async_api
async def test_negative_price_and_oversized_page_are_rejected(api: ApiHarness):
    negative = await api.client.post(
        '/api/products/',
        json={'name': 'Bad', 'slug': 'bad', 'price': -1},
    )
    oversized = await api.client.get('/api/products/', params={'limit': 1000})
    assert negative.status_code == 422
    assert oversized.status_code == 422


@async_api
async def test_deactivated_product_is_hidden(api: ApiHarness):
    created = await create_product(api.client, slug='hidden-carrot')
    deleted = await api.client.delete(f"/api/products/{created['id']}")
    assert deleted.status_code == 200
    assert deleted.json()['is_active'] is False

    listing = await api.client.get('/api/products/')
    by_id = await api.client.get(f"/api/products/{created['id']}")
    assert listing.json() == []
    assert by_id.status_code == 404
    assert by_id.json()['detail'] == 'Product not found'

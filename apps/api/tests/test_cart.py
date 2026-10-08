from decimal import Decimal

from tests.api import ApiHarness, async_api, create_product, register_and_login


@async_api
async def test_cart_requires_authentication(api: ApiHarness):
    response = await api.client.get('/api/cart/')
    assert response.status_code == 401


@async_api
async def test_empty_cart_is_not_found(api: ApiHarness):
    headers = await register_and_login(api.client)
    response = await api.client.get('/api/cart/', headers=headers)
    assert response.status_code == 404


@async_api
async def test_item_price_comes_from_the_catalog(api: ApiHarness):
    headers = await register_and_login(api.client)
    product = await create_product(api.client, price=10.5)

    added = await api.client.post(
        '/api/cart/items',
        headers=headers,
        json={'product_id': product['id'], 'quantity': 2, 'price': '0.01'},
    )
    assert added.status_code == 200, added.text
    items = added.json()['items']
    assert len(items) == 1
    assert items[0]['product_id'] == product['id']
    assert items[0]['quantity'] == 2
    assert Decimal(items[0]['price']) == Decimal('10.50')

    replaced = await api.client.post(
        '/api/cart/items',
        headers=headers,
        json={'product_id': product['id'], 'quantity': 4},
    )
    assert replaced.status_code == 200
    replaced_items = replaced.json()['items']
    assert len(replaced_items) == 1
    assert replaced_items[0]['id'] == items[0]['id']
    assert replaced_items[0]['quantity'] == 4
    assert Decimal(replaced_items[0]['price']) == Decimal('10.50')


@async_api
async def test_patch_updates_the_cart_item_rather_than_a_product_id(api: ApiHarness):
    headers = await register_and_login(api.client)
    first = await create_product(api.client, name='Cucumber', slug='cucumber', price=5)
    second = await create_product(api.client, name='Tomato', slug='tomato', price=9)
    added = await api.client.post(
        '/api/cart/items',
        headers=headers,
        json={'product_id': second['id'], 'quantity': 1},
    )
    item = added.json()['items'][0]
    assert item['id'] != second['id']

    updated = await api.client.patch(
        f"/api/cart/items/{item['id']}",
        headers=headers,
        json={'quantity': 3},
    )
    assert updated.status_code == 200, updated.text
    items = updated.json()['items']
    assert len(items) == 1
    assert items[0]['id'] == item['id']
    assert items[0]['product_id'] == second['id']
    assert items[0]['product_id'] != first['id']
    assert items[0]['quantity'] == 3
    assert Decimal(items[0]['price']) == Decimal('9.00')


@async_api
async def test_missing_product_and_missing_item_return_404(api: ApiHarness):
    headers = await register_and_login(api.client)
    missing_product = await api.client.post(
        '/api/cart/items',
        headers=headers,
        json={'product_id': 999, 'quantity': 1},
    )
    assert missing_product.status_code == 404

    product = await create_product(api.client)
    added = await api.client.post(
        '/api/cart/items',
        headers=headers,
        json={'product_id': product['id'], 'quantity': 1},
    )
    item_id = added.json()['items'][0]['id']
    missing_item = await api.client.patch(
        f'/api/cart/items/{item_id + 100}',
        headers=headers,
        json={'quantity': 2},
    )
    assert missing_item.status_code == 404


@async_api
async def test_delete_item_and_reject_inactive_product(api: ApiHarness):
    headers = await register_and_login(api.client)
    product = await create_product(api.client, slug='cabbage')
    added = await api.client.post(
        '/api/cart/items',
        headers=headers,
        json={'product_id': product['id'], 'quantity': 1},
    )
    item_id = added.json()['items'][0]['id']

    removed = await api.client.delete(f'/api/cart/items/{item_id}', headers=headers)
    assert removed.status_code == 200
    assert removed.json()['items'] == []

    await api.client.delete(f"/api/products/{product['id']}")
    inactive = await api.client.post(
        '/api/cart/items',
        headers=headers,
        json={'product_id': product['id'], 'quantity': 1},
    )
    assert inactive.status_code == 404

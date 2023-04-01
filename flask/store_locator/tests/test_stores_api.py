import pytest

@pytest.fixture()
def new_store(session, client):
    return client.post('/stores', json={
        'name': 'Super Store',
        'street_address': '100 Road Place',
        'city': 'Boston',
        'state': 'MA',
        'zip_code': '10204',
        'latitude': 42.3601,
        'longitude': -71.0589
    })

@pytest.fixture()
def new_member(session, client):
    return client.post('/members', json={
        'name': 'Vincent Wixsom',
        'email': 'vincent.wixsom@gmail.com',
        'password': 'supersecretpassword!'
    })

@pytest.fixture()
def new_vendor(session, new_member, client):
    return client.post('/vendors', json={
        'name': 'Niche Foods, Inc.',
        'street_address': '100 Highway Ln',
        'city': 'Springfield',
        'state': 'MA',
        'zip_code': '10102',
        'member_id': new_member.json['id']
    })


@pytest.fixture()
def new_product(session, new_vendor, client):
    return client.post('/products', json={
        'name': 'Sunflower Seeds',
        'description': 'Pretty good seeds.',
        'price': 7.99,
        'vendor_id': new_vendor.json['id']
    })

def test_create_store(new_store):
    assert new_store.json['name'] == 'Super Store'
    assert new_store.json['street_address'] == '100 Road Place'
    assert new_store.json['city'] == 'Boston'
    assert new_store.json['state'] == 'MA'
    assert new_store.json['zip_code'] == '10204'
    assert new_store.json['latitude'] == 42.3601
    assert new_store.json['longitude'] == -71.0589

def test_get_existing_store(new_store, client):
    response = client.get(f'/stores/{new_store.json["id"]}')

    assert response.json['name'] == 'Super Store'
    assert response.json['street_address'] == '100 Road Place'
    assert response.json['city'] == 'Boston'
    assert response.json['state'] == 'MA'
    assert response.json['zip_code'] == '10204'
    assert response.json['latitude'] == 42.3601
    assert response.json['longitude'] == -71.0589

def test_update_store(new_store, client):
    response = client.patch(f'/stores/{new_store.json["id"]}', json={
        "name": "Mega Test Store",
        "latitude": 44.3601,
        "longitude": -73.0589
    })

    assert response.json['name'] == 'Mega Test Store'
    assert response.json['latitude'] == 44.3601
    assert response.json['longitude'] == -73.0589

def test_delete_store(new_store, client):
    response = client.delete(f'/stores/{new_store.json["id"]}')

    assert response.get_data(as_text=True) == 'true\n'

def test_add_vendor_to_store(new_vendor, new_store, client):
    response = client.post(f'/stores/{new_store.json["id"]}/vendor/{new_vendor.json["id"]}')

    assert response.get_data(as_text=True) == 'true\n'

def test_remove_vendor_from_store(new_vendor, new_store, client):
    client.post(f'/stores/{new_store.json["id"]}/vendor/{new_vendor.json["id"]}')
    response = client.delete(f'/stores/{new_store.json["id"]}/vendor/{new_vendor.json["id"]}')

    assert response.get_data(as_text=True) == 'true\n'

def test_get_vendors_for_store(new_vendor, new_store, client):
    client.post(f'/stores/{new_store.json["id"]}/vendor/{new_vendor.json["id"]}')
    response = client.get(f'/stores/{new_store.json["id"]}/vendors')

    assert len(response.json) == 1

def test_add_product_to_store(new_vendor, new_store, new_product, client):
    # vendor must be added to store before vendor's products can be added to the store
    client.post(f'/stores/{new_store.json["id"]}/vendor/{new_vendor.json["id"]}')
    response = client.post(f'/stores/{new_store.json["id"]}/product/{new_product.json["id"]}')

    assert response.get_data(as_text=True) == 'true\n'

def test_remove_product_from_store(new_store, new_product, new_vendor, client):
    # add vendor and product to store
    client.post(f'/stores/{new_store.json["id"]}/vendor/{new_vendor.json["id"]}')
    client.post(f'/stores/{new_store.json["id"]}/product/{new_product.json["id"]}')
    response = client.delete(f'/stores/{new_store.json["id"]}/product/{new_product.json["id"]}')

    assert response.get_data(as_text=True) == 'true\n'

def test_get_products_for_store(new_product, new_vendor, new_store, client):
    # add vendor and product to store
    client.post(f'/stores/{new_store.json["id"]}/vendor/{new_vendor.json["id"]}')
    client.post(f'/stores/{new_store.json["id"]}/product/{new_product.json["id"]}')
    response = client.get(f'/stores/{new_store.json["id"]}/products')

    assert len(response.json) == 1

def test_get_stores_for_product(new_store, new_product, new_vendor, client):
    client.post(f'/stores/{new_store.json["id"]}/vendor/{new_vendor.json["id"]}')
    client.post(f'/stores/{new_store.json["id"]}/product/{new_product.json["id"]}')
    response = client.get(f'/products/{new_product.json["id"]}/stores')

    assert len(response.json) == 1
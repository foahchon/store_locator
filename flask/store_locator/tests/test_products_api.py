import pytest

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

def test_create_product(new_product, new_vendor):
    assert new_product.json['description'] == 'Pretty good seeds.'
    assert new_product.json['id'] > 0
    assert new_product.json['name'] == 'Sunflower Seeds'
    assert new_product.json['price'] == 7.99
    assert new_product.json['vendor_id'] == new_vendor.json['id']

def test_update_product(new_product, client):
    response = client.patch(f'/products/{new_product.json["id"]}', json={
        'name': 'Flax Cereal',
        'description': 'Pretty good cereal.',
        'price': 3.99
    })

    assert response.json['name'] == 'Flax Cereal'
    assert response.json['description'] == 'Pretty good cereal.'
    assert response.json['price'] == 3.99

def test_delete_product(new_product, client):
    response = client.delete(f'/products/{new_product.json["id"]}')
    
    assert response.get_data(as_text=True) == 'true\n'

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


def test_create_vendor(new_member, new_vendor):
    assert new_vendor.json['name'] == 'Niche Foods, Inc.'
    assert new_vendor.json['street_address'] == '100 Highway Ln'
    assert new_vendor.json['city'] == 'Springfield'
    assert new_vendor.json['state'] == 'MA'
    assert new_vendor.json['zip_code'] == '10102'
    assert new_vendor.json['member_id'] == new_member.json['id']

def test_get_existing_vendor(new_vendor, client):
    response = client.get(f'/vendors/{new_vendor.json["id"]}')

def test_update_vendor(session, new_vendor, client):
    response = client.patch(f'/vendors/{new_vendor.json["id"]}', json={
        'name': 'Test Company, LLC'
    })

    assert response.json['name'] == 'Test Company, LLC'


def test_delete_vendor(new_vendor, client):
    response = client.delete(f'/vendors/{new_vendor.json["id"]}')

    assert response.get_data(as_text=True) == 'true\n'

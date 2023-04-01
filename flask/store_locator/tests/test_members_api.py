import pytest

@pytest.fixture()
def new_member(session, client):
    return client.post('/members', json={
        'name': 'Vincent Wixsom',
        'email': 'vincent.wixsom@gmail.com',
        'password': 'supersecretpassword!'
    })

def test_create_member(new_member):
    assert new_member.json['name'] == 'Vincent Wixsom'
    assert new_member.json['email'] == 'vincent.wixsom@gmail.com'
    assert new_member.json['id'] > 0

def test_get_existing_member(new_member, client):
    response = client.get(f'/members/{new_member.json["id"]}')

    assert response.json['id'] == new_member.json['id']

def test_update_member(new_member, client):
    response = client.patch(f'/members/{new_member.json["id"]}', json={
        'email': 'testuser@test.com',
        'name': 'Test McUser',
        'password': 'supersecretpassword!'
    })

    assert response.json['email'] == 'testuser@test.com'
    assert response.json['name'] == 'Test McUser'
    assert response.json['id'] == new_member.json['id']

def test_delete_member(new_member, client):
    response = client.delete(f'/members/{new_member.json["id"]}')

    assert response.get_data(as_text=True) == 'true\n'
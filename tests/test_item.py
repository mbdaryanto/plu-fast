from fastapi.testclient import TestClient
from plu_app.main import app


def test_get_item():
    client = TestClient(app)
    response = client.get('/item', params={'code': '90005010'})
    assert response.status_code == 200
    print(repr(response.json()))

    response = client.get('/item', params={'code': '8997227891295'})
    assert response.status_code == 200
    print(repr(response.json()))

    response = client.get('/item', params={'code': 'NOOOOO'})
    assert response.status_code == 404
    print(repr(response.json()))

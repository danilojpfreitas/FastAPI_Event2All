from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_user():
    response = client.get('/user')

    assert response.status_code == 200
    assert response.json() == [
        {}
    ]


def tes0t_post_user():
    new_user = {
        "name": "string",
        "email": "string",
        "password": "string",
        "createdAt": 0,
        "updatedAt": 0
    }

    response = client.post('/user', json=new_user)
    assert response.status_code == 201

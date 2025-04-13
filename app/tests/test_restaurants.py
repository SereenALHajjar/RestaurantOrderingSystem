
def assert_restaurant_equal(expected, actual):
    for key in ["name", "email", "phone", "password"]:
        assert expected[key] == actual[key]

def test_get_restaurants(client):
    payload_0 = {
        "name": "KFC",
        "email": "KFC@example.com",
        "password": "secure123",
        "phone": "1234567890"
    }
    payload_1 = {
        "name": "MC",
        "email": "MC@example.com",
        "password": "secure123",
        "phone": "1234567880"
    }
    client.post("/restaurants/",  json=payload_0)
    client.post("/restaurants/",  json=payload_1)
    response = client.get("/restaurants")
    assert response.status_code == 200
    assert_restaurant_equal(payload_0 , response.json()[0])
    assert_restaurant_equal(payload_1 , response.json()[1])


def test_get_specific_restaurant(client):
    payload = {
        "name": "KFC",
        "email": "KFC@example.com",
        "password": "secure123",
        "phone": "1234567890"
    }
    client.post("/restaurants/",  json=payload)
    response = client.get("/restaurants/1")
    # print(response.json())
    assert response.status_code == 200
    assert_restaurant_equal(payload , response.json())
    assert response.json()["id"] == 1


def test_get_specific_restaurant_failed(client):
    response = client.get("/restaurants/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "No such Restaurant"


def test_add_restaurant_success(client):
    payload = {
        "name": "KFC",
        "email": "KFC@example.com",
        "password": "secure123",
        "phone": "1234567890"
    }
    response = client.post("/restaurants/", json=payload)
    assert response.status_code == 200
    assert_restaurant_equal(payload , response.json())
    assert response.json()["id"] == 1


def test_add_restaurant_failed(client):
    payload = {
        "name": "KFC",
        "email": "KFC@example.com",
        "password": "secure123",
        "phone": "1234567890"
    }
    client.post("/restaurants/", json=payload)
    response = client.post("/restaurants/", json=payload)
    assert response.status_code == 400 
    assert response.json()["detail"] == "Restaurant with this email already exist"
import os
import io
import shutil


def create_dummy_image():
    return io.BytesIO(b"fake image data")


def create_restaurant(client):
    client.post("/restaurants/", json={
                "name": "MC",
                "email": "MC@example.com",
                "password": "secure123",
                "phone": "1234567880"
                })
def create_recipe(client ,payload):
    image_file = create_dummy_image()
    image_file.name = "test.jpg"
    
    response = client.post(
        "/recipes/",
        data=payload,
        files={"photo": ("test.jpg", image_file, "image/jpeg")}
    )
    return response
def create_recipe_without_image(client ,payload):
    response = client.post(
        "/recipes/",
        data=payload, 
    )
    return response

def assert_recipe_equal(expected, actual):
    for key in ["name", "description", "price", "category"]:
        assert expected[key] == actual[key]


def test_add_recipe_success(client):
    create_restaurant(client)
    payload = {
        "name": "Pizza",
        "description": "Cheesy and hot",
        "price": 9.99,
        "category": "Italian",
        "restaurant_id": 1
    }
    response = create_recipe(client , payload)
    assert response.status_code == 200
    data = response.json()
    assert_recipe_equal(data, payload)
    assert "photo" in data


def test_get_all_recipes(client):
    create_restaurant(client)
    payload = {
        "name": "Pizza",
        "description": "Cheesy and hot",
        "price": 9.99,
        "category": "Italian",
        "restaurant_id": 1
    }
    create_recipe(client , payload)
    response = client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert_recipe_equal(data[0] , payload)
    assert "photo" in data[0]

def test_get_specific_recipe(client):
    payload = {
        "name": "Pizza",
        "description": "Cheesy and hot",
        "price": 9.99,
        "category": "Italian",
        "restaurant_id": 1
    }
    create_restaurant(client)
    create_recipe(client , payload)
    response = client.get("/recipes/1")
    assert response.status_code == 200
    assert_recipe_equal(response.json() , payload)

def test_get_specific_recipe_failed(client):
    response = client.get("/recipes/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "No such recipe"

def test_get_specific_recipe_photo(client):
    create_restaurant(client)
    payload = {
        "name": "Pizza",
        "description": "Cheesy and hot",
        "price": 9.99,
        "category": "Italian",
        "restaurant_id": 1
    }
    create_recipe(client , payload)
    response = client.get("/recipes/get-photo/1")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/")

def test_get_specific_recipe_photo_failed_no_photo(client):
    create_restaurant(client)
    payload = {
        "name": "Pizza",
        "description": "Cheesy and hot",
        "price": 9.99,
        "category": "Italian",
        "restaurant_id": 1, 
    }
    res = create_recipe_without_image(client , payload)
    print(res.json())
    response = client.get(f"/recipes/get-photo/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "No photo for this recipe"


 



def test_create_user(client):
    payload = {
        "name": "Sereen",
        "email": "sereen@example.com",
        "password": "secure123",
        "phone": "1234567890",
        "birth_date": "1999-01-01"
    }

    response = client.post("/users/signup", json=payload)
    data = response.json()

    assert response.status_code == 200
    for key in ["name", "email", "phone", "birth_date"]:
        assert data[key] == payload[key]
    assert "id" in data
    
    # Duplicated email
    response2 = client.post("/users/signup", json=payload)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "User with this email already exists"
    
# def test_signup_missing_fields(client):
#     payload = {
#         "name": "Sereen"
#         # missing email, password, etc.
#     }
#     response = client.post("/users/signup", json=payload)
#     assert response.status_code == 500  # Unprocessable Entity

def test_login_success(client):
    signup_data = {
        "name": "Sereen",
        "email": "sereen@example.com",
        "password": "secure123",
        "phone": "1234567890",
        "birth_date": "1999-01-01"
    }
    client.post("/users/signup", json=signup_data)

    login_data = {
        "email": "sereen@example.com",
        "password": "secure123"
    }
    response = client.post("/users/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["user"]["email"] == login_data["email"]

def test_login_invalid_password(client):
    signup_data = {
        "name": "Sereen",
        "email": "sereen@example.com",
        "password": "secure123",
        "phone": "1234567890",
        "birth_date": "1999-01-01"
    }
    client.post("/users/signup", json=signup_data)

    # wrong password
    response = client.post("/users/login", json={
        "email": "sereen@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email or password"

def test_get_user_success(client):
    signup_data = {
        "name": "Sereen",
        "email": "sereen@example.com",
        "password": "secure123",
        "phone": "1234567890",
        "birth_date": "1999-01-01"
    }
    client.post("/users/signup", json=signup_data)
    
    response = client.get('/users/1')
    assert response.status_code == 200 
    for key in ["name", "email", "phone", "birth_date"]:
        assert signup_data[key] == response.json()[key]
    assert "id" in response.json()
    
def test_get_user_failed(client):
    response = client.get('/users/1')
    assert response.status_code == 404
    assert response.json()["detail"] == "No such user" 
    
    
    
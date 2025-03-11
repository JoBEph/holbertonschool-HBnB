import pytest
from app.models.user import User
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_user():
    user = User("John", "Doe", "john.doe@example.com", is_admin=True)
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is True
    assert user.place == []

def test_first_name_validation():
    with pytest.raises(TypeError, match="first name must be a non-empty string"):
        User(123, "Doe", "john.doe@example.com")
    
    with pytest.raises(TypeError, match="first name must be a non-empty string"):
        User("", "Doe", "john.doe@example.com")
    
    with pytest.raises(ValueError, match="first name is too long"):
        User("J" * 51, "Doe", "john.doe@example.com")

def test_last_name_validation():
    with pytest.raises(TypeError, match="last name must be a non-empty string"):
        User("John", 456, "john.doe@example.com")
    
    with pytest.raises(TypeError, match="last name must be a non-empty string"):
        User("John", "", "john.doe@example.com")
    
    with pytest.raises(ValueError, match="last name is too long"):
        User("John", "D" * 51, "john.doe@example.com")

def test_email_validation():
    with pytest.raises(TypeError, match="email must be a string"):
        User("John", "Doe", 12345)
    
    with pytest.raises(TypeError, match="email is required"):
        User("John", "Doe", "")
    
    with pytest.raises(ValueError, match="email format is incorrect"):
        User("John", "Doe", "invalid-email")

def test_is_admin_validation():
    with pytest.raises(TypeError, match="Admin must be True or False"):
        User("John", "Doe", "john.doe@example.com", is_admin="yes")

def test_display():
    user = User("Alice", "Smith", "alice.smith@example.com")
    expected_output = {
        "id": user.id,
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com"
    }
    assert user.display() == expected_output

def test_add_place():
    user = User("John", "Doe", "john.doe@example.com")
    user.add_place("Paris")
    assert "Paris" in user.place

def test_create_user_api(client):
    response = client.post("/api/v1/users/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["first_name"] == "John"
    assert response.json["last_name"] == "Doe"
    assert response.json["email"] == "john.doe@example.com"

def test_create_user_invalid_api(client):
    response = client.post("/api/v1/users/", json={
        "first_name": "",
        "last_name": "",
        "email": "wrong-email"
    })
    assert response.status_code == 400
    assert response.json == {"message": "invalid input data"}

def test_get_all_users(client):
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_user_by_id(client):
    response = client.post("/api/v1/users/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com"
    })
    user_id = response.json["id"]
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json["first_name"] == "Alice"
    assert response.json["last_name"] == "Smith"

def test_update_user(client):
    response = client.post("/api/v1/users/", json={
        "first_name": "Bob",
        "last_name": "Marley",
        "email": "bob.marley@example.com"
    })
    user_id = response.json["id"]
    response = client.put(f"/api/v1/users/{user_id}", json={
        "first_name": "Bobby"
    })
    assert response.status_code == 201
    assert response.json["first_name"] == "Bobby"

def test_delete_user(client):
    response = client.post("/api/v1/users/", json={
        "first_name": "Charlie",
        "last_name": "Chaplin",
        "email": "charlie@example.com"
    })
    user_id = response.json["id"]
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404

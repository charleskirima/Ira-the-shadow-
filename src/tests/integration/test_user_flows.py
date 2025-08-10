import pytest
from flask import Flask
from src.web.routes.auth import auth  # Adjust as necessary

@pytest.fixture
def app_client():
    """
    Sets up a Flask test client with the authentication blueprint.
    """
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(auth)

    with app.test_client() as client:
        yield client

def test_user_registration_and_login(app_client):
    test_username = "testuser"
    test_password = "testpass"

    # Step 1: Register the user
    res_register = app_client.post("/auth/register", json={
        "username": test_username,
        "password": test_password
    })

    assert res_register.status_code in (200, 201), f"Register failed: {res_register.status_code} - {res_register.data.decode()}"

    # Step 2: Log the user in
    res_login = app_client.post("/auth/login", json={
        "username": test_username,
        "password": test_password
    })

    assert res_login.status_code == 200, f"Login failed: {res_login.status_code} - {res_login.data.decode()}"
    data = res_login.get_json()

    assert data is not None, "Login response is not JSON"
    assert any(k in data for k in ["token", "user"]), "Missing 'token' or 'user' in response"

    if "user" in data:
        assert isinstance(data["user"], dict), "'user' key should contain a user object"
        assert "username" in data["user"], "'username' missing in user object"
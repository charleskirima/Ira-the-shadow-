import pytest
from flask import Flask
from src.web.routes.chat import chat

@pytest.fixture
def client():
    """
    Creates a test client with the chat blueprint registered.
    """
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(chat)

    assert app.testing, "App not in TESTING mode"

    with app.test_client() as client:
        yield client

def test_chat_response(client):
    """
    Ensures /chat/ endpoint responds correctly with JSON and includes a 'response' key.
    """
    payload = {
        "message": "I feel stuck",
        "context": {}
    }

    response = client.post("/chat/", json=payload)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert response.is_json, "Response is not in JSON format"

    data = response.get_json()
    assert "response" in data, "Missing 'response' key in response JSON"
    assert isinstance(data["response"], str), "'response' should be a string"
    assert len(data["response"].strip()) > 0, "'response' is empty"
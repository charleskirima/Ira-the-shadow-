import pytest
from flask import Flask

@pytest.fixture(scope="session")
def test_config():
    """
    Returns a shared config dictionary for tests.
    Extend as needed.
    """
    return {
        "test_mode": True,
        "default_user": {
            "username": "ira_test",
            "password": "test123"
        }
    }

@pytest.fixture(scope="session")
def test_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client
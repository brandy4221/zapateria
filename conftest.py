import pytest
from Back import app  # Cambia "Back" si tu archivo principal tiene otro nombre

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_mysql(monkeypatch):
    from unittest.mock import MagicMock
    mock = MagicMock()
    monkeypatch.setattr('Back.mysql', mock)
    return mock

import pytest
from Back import app  # Asegúrate de que Back.py es el nombre correcto de tu archivo principal

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

# tests/test_app.py

import pytest
from app import app  # o from back import app, si tu archivo se llama back.py

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

def test_home_redirects_to_login(client):
    response = client.get('/')
    assert response.status_code == 302  # Redirección
    assert '/login' in response.headers['Location']

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Ingresar' in response.data  # Verifica que el botón esté presente

def test_api_productos(client):
    response = client.get('/api/productos')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_healthz(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert b'OK' in response.data

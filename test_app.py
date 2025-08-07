import pytest
from werkzeug.security import generate_password_hash

def setup_mock_cursor(mock_mysql, user_data=None, multiple_rows=None):
    mock_cursor = mock_mysql.connection.cursor.return_value
    if user_data:
        mock_cursor.fetchone.return_value = user_data
    else:
        mock_cursor.fetchone.return_value = None

    if multiple_rows:
        mock_cursor.fetchall.return_value = multiple_rows
    else:
        mock_cursor.fetchall.return_value = []

# ----------- TEST LOGIN EXITOSO ------------

def test_api_login_success(client, mock_mysql):
    password = 'password123'
    hashed = generate_password_hash(password)
    mock_user = {
        'id': 1,
        'nombre': 'Test User',
        'email': 'test@example.com',
        'password': hashed,
        'rol': 'cliente'
    }
    setup_mock_cursor(mock_mysql, user_data=mock_user)

    data = {
        'email': 'test@example.com',
        'clave': password
    }

    response = client.post('/api/login', json=data)

    assert response.status_code == 200
    assert 'token' in response.get_json()

# ----------- TEST LOGIN FALLIDO ------------

def test_api_login_failure(client, mock_mysql):
    setup_mock_cursor(mock_mysql)  # Sin usuario

    data = {
        'email': 'fail@example.com',
        'clave': 'wrongpassword'
    }

    response = client.post('/api/login', json=data)

    assert response.status_code == 401
    assert 'error' in response.get_json()

# ----------- TEST API PRODUCTOS ------------

def test_api_productos(client, mock_mysql):
    mock_productos = [
        {'id': 1, 'nombre': 'Zapato', 'precio': 100},
        {'id': 2, 'nombre': 'Bota', 'precio': 200}
    ]
    setup_mock_cursor(mock_mysql, multiple_rows=mock_productos)

    response = client.get('/api/productos')

    assert response.status_code == 200
    assert response.get_json() == mock_productos

# ----------- TEST VISTAS FLASK ------------

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'<form' in response.data

def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code in (200, 302)

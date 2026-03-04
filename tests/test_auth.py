import pytest
from app.main import create_app
from app.database import db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post('/api/v1/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'Password123'
    })
    
    assert response.status_code == 201
    assert 'access_token' in response.json
    assert 'user' in response.json

def test_login(client):
    # First register
    client.post('/api/v1/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'Password123'
    })
    
    # Then login
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'Password123'
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json
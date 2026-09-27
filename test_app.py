import pytest
from app import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    init_db()
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Student Management System" in response.data

def test_add_student(client):
    response = client.post('/add', data=dict(
        name="John Doe",
        email="john@example.com",
        course="Computer Science"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"John Doe" in response.data
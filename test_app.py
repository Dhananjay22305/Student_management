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

def test_add_and_search_student(client):
    # Test Adding a Student
    add_response = client.post('/add', data=dict(
        name="Jane Doe",
        email="jane@example.com",
        course="DevOps"
    ), follow_redirects=True)
    assert add_response.status_code == 200
    assert b"Jane Doe" in add_response.data

    # Test Searching for Student
    search_response = client.get('/?search=Jane')
    assert b"Jane Doe" in search_response.data

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

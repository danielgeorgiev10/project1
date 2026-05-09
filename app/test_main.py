import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_fibonacci_base_cases(client):
    # F(0) = 0
    res0 = client.get('/fibonacci/0')
    assert res0.json['result'] == 0
    
    # F(1) = 1
    res1 = client.get('/fibonacci/1')
    assert res1.json['result'] == 1

def test_fibonacci_calculation(client):
    res = client.get('/fibonacci/10')
    assert res.status_code == 200
    assert res.json['result'] == 55

def test_fibonacci_too_large(client):
    res = client.get('/fibonacci/101')
    assert res.status_code == 400
    assert "error" in res.json

def test_index_page(client):
    res = client.get('/')
    assert res.status_code == 200
    assert "Welcome to Project-App API!" in res.json['message']
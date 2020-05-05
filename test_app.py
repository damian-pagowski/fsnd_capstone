'''
Tests for jwt flask app.
'''
import os
import json
import pytest

import app

SECRET = 'TestSecret'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjEzMDY3OTAsIm5iZiI6MTU2MDA5NzE5MCwiZW1haWwiOiJ3b2xmQHRoZWRvb3IuY29tIn0.IpM4VMnqIgOoQeJxUbLT-cRcAjK41jronkVrqRLFmmk'
EMAIL = 'wolf@thedoor.com'
PASSWORD = 'huff-puff'

@pytest.fixture
def client():
    # os.environ['JWT_SECRET'] = SECRET
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    yield client

def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200



def test_login_success_page(client):
    response = client.get('/login-success')
    assert response.status_code == 200



# def test_health(client):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert response.json == 'Healthy'

# def test_auth(client):
#     body = {'email': EMAIL,
#             'password': PASSWORD}
#     response = client.post('/auth', 
#                            data=json.dumps(body),
#                            content_type='application/json')

#     assert response.status_code == 200
#     token = response.json['token']
#     assert token is not None




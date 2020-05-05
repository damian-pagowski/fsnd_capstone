

import os
import json
import pytest

import http.client

SECRET = ''
TOKEN = ''
EMAIL = ''
PASSWORD = ''

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client


def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200

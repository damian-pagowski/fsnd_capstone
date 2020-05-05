'''
Tests for jwt flask app.
'''
import os
import json
import pytest
import random
import app

ASSISTANT_TOKEN = os.environ.get('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.environ.get('PRODUCER_TOKEN')


@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    client = app.app.test_client()
    yield client


def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_success_page(client):
    response = client.get('/login-success')
    assert response.status_code == 200


def test_asistant_can_list_actors(client):
    print(ASSISTANT_TOKEN)
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)
    }
    response = client.get('/actors', headers=headers)
    assert response.status_code == 200


def test_asistant_can_list_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)
    }
    response = client.get('/movies',  headers=headers)
    assert response.status_code == 200


def test_asistant_can_not_create_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)}
    response = client.post('/movies',  headers=headers,
                           content_type='application/json',
                           data=json.dumps(dict(
                               relese_date='2020',
                               title='Rambo 123456'
                           )),
                           )
    assert response.status_code == 403


def test_asistant_can_not_create_actors(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)}
    response = client.post('/actors',  headers=headers,
                           content_type='application/json',
                           data=json.dumps(dict(
                               age=70,
                               gender="M",
                               movie_id=1,
                               name="Van Damme"
                           )),
                           )
    assert response.status_code == 403


def test_asistant_can_not_delete_actors(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)}
    response = client.delete('/actors/1',  headers=headers)
    assert response.status_code == 403


def test_asistant_can_not_delete_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)}
    response = client.delete('/movies/1',  headers=headers)
    assert response.status_code == 403


def test_asistant_can_not_update_actors(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)}
    response = client.patch('/actors/1',  headers=headers,
                            content_type='application/json',
                            data=json.dumps(dict(
                                age=99,
                            )),
                            )
    assert response.status_code == 403

def test_asistant_can_not_update_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)}
    response = client.patch('/movies/1',  headers=headers,
                           content_type='application/json',
                           data=json.dumps(dict(
                               title="Bloodsport XXV"
                           )),
                           )
    assert response.status_code == 403

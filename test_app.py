'''
Tests for jwt flask app.
'''
import os
import json
import pytest
import random
import app
from database.models import db, Movie, Actor

ASSISTANT_TOKEN = os.environ.get('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.environ.get('PRODUCER_TOKEN')


@pytest.fixture
def client():
    database_filename = 'test.db'
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = "sqlite:///{}".format(
        os.path.join(project_dir, database_filename))
    app.app.config['TESTING'] = True
    app.app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    client = app.app.test_client()
    db.drop_all()
    db.create_all()
    yield client


def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_success_page(client):
    response = client.get('/login-success')
    assert response.status_code == 200


# Assistant role

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
    response = client.get('/movies', headers=headers)
    assert response.status_code == 200


def test_asistant_can_not_create_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)}
    response = client.post('/movies', headers=headers,
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
    response = client.post('/actors', headers=headers,
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
    response = client.delete('/actors/1', headers=headers)
    assert response.status_code == 403


def test_asistant_can_not_delete_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)}
    response = client.delete('/movies/1', headers=headers)
    assert response.status_code == 403


def test_asistant_can_not_update_actors(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)}
    response = client.patch('/actors/1', headers=headers,
                            content_type='application/json',
                            data=json.dumps(dict(
                                age=99,
                            )),
                            )
    assert response.status_code == 403


def test_asistant_can_not_update_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)}
    response = client.patch('/movies/1', headers=headers,
                            content_type='application/json',
                            data=json.dumps(dict(
                                title="Bloodsport XXV"
                            )),
                            )
    assert response.status_code == 403


# producer

# producer > movies


def test_producer_can_list_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(PRODUCER_TOKEN)
    }
    response = client.get('/movies', headers=headers)
    assert response.status_code == 200


def test_producer_can_create_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(PRODUCER_TOKEN)}
    response = client.post('/movies', headers=headers,
                           content_type='application/json',
                           data=json.dumps(dict(
                               relese_date='2099',
                               title='Terminator 123456'
                           )),
                           )
    assert response.status_code == 200


def test_producer_can_update_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(PRODUCER_TOKEN)}
    response = client.patch("/movies/1", headers=headers,
                            content_type='application/json',
                            data=json.dumps(dict(
                                relese_date='summer 2100',

                            )),
                            )
    assert response.status_code == 200
    assert response.get_json()['movie']['relese_date'] == 'summer 2100'


def test_producer_can_delete_movies(client):
    headers = {
        'Authorization': 'Bearer {}'.format(PRODUCER_TOKEN)}
    response = client.delete("/movies/1", headers=headers)
    assert response.status_code == 200

# producer > actors


actor_id = 0


def test_producer_can_list_actors(client):
    print(ASSISTANT_TOKEN)
    headers = {
        'Authorization': 'Bearer {}'.format(PRODUCER_TOKEN)
    }
    response = client.get('/actors', headers=headers)
    assert response.status_code == 200


def test_producer_can_create_actors(client):
    headers = {
        'Authorization': 'Bearer {}'.format(PRODUCER_TOKEN)}
    response = client.post('/actors', headers=headers,
                           content_type='application/json',
                           data=json.dumps(dict(
                               age=71,
                               gender="M",
                               movie_id=1,
                               name="Van Damme Junior"
                           )),
                           )
    assert response.status_code == 200


def test_producer_can_update_actors(client):
    headers = {
        'Authorization': 'Bearer {}'.format(PRODUCER_TOKEN)}
    body = json.dumps(dict(age=150))
    response = client.patch("/actors/1", headers=headers,
                            content_type='application/json',
                            data=body
                            )
    assert response.status_code == 200
    assert response.get_json()['actor']['age'] == 150


def test_producer_can_delete_actors(client):
    headers = {
        'Authorization': 'Bearer {}'.format(PRODUCER_TOKEN)}
    response = client.delete("/actors/1", headers=headers)
    assert response.status_code == 200

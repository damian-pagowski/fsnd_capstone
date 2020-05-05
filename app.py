import os
from flask import Flask, request, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db, Actor, Movie
from sqlalchemy import exc
from auth.auth import AuthError, requires_auth
import json
import sys


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    return app


app = create_app()
setup_db(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# recreate db
FLASK_ENV = os.environ.get("FLASK_ENV", "NOT_DEV")
print("MODE: " + FLASK_ENV)
if FLASK_ENV != "development":
    print("Recreating database")
    db_drop_and_create_all()


@app.route('/', methods=['GET'])
def hello():
    error = False
    error_message = "Set required environment variables before run: "
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    if AUTH0_DOMAIN == None:
      error = True
      error_message += "AUTH0_DOMAIN"
    AUTH0_AUDIENCE = os.environ.get('AUTH0_AUDIENCE')
    if AUTH0_AUDIENCE == None:
      error = True
      error_message += "AUTH0_AUDIENCE"
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    if AUTH0_CLIENT_ID == None:
      error = True
      error_message += "AUTH0_CLIENT_ID"
    AUTH0_CB_URL = os.environ.get('AUTH0_CB_URL')
    if AUTH0_CB_URL == None:
      error = True
      error_message += "AUTH0_CB_URL"
    if error:
      print(error_message)

    link = "https://"
    link += AUTH0_DOMAIN
    link += "/authorize?"
    link += "audience=" + AUTH0_AUDIENCE + "&"
    link += "response_type=token&"
    link += "client_id=" + AUTH0_CLIENT_ID + "&"
    link += "redirect_uri=" + AUTH0_CB_URL
    print("URL: " + link)
    return render_template('index.html', login_url=link)


@app.route('/login-success', methods=['GET'])
def login_success():
    return render_template('login_success.html')

##########################################
#   ACTORS
##########################################

#  GET /actors
@app.route('/actors')
@requires_auth('get:actors')
def get_actors(payload):
    print(payload)
    actors = []
    print("/actors")
    try:
        actors_data = Actor.query.all()
        actors = list(map(Actor.format, actors_data))
    except:
        abort(422)
    return jsonify({
        'success': True,
        'actors': actors
    })

#  POST /actors
@app.route('/actors', methods=['POST'])
@requires_auth('create:actors')
def create_actor(payload):
    try:
        # params from request
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        movie_id = body.get('movie_id')
        #
        actor = Actor(name, age, gender, movie_id)
        print(actor.format())
        actor.insert()
        return jsonify({"success": True, "actor": actor.format()})
    except:
        abort(422)

#  DELETE /actors
@app.route('/actors/<id>', methods=['DELETE'])
@requires_auth('delete:actors')
def remove_actor(payload, id):
    try:
        actor = Actor.query.get(id)
        actor.delete()
        return jsonify({"success": True, "status": "deleted"})
    except:
        abort(422)

#  PATCH /actors
@app.route('/actors/<id>', methods=['PATCH'])
@requires_auth('update:actors')
def update_actor(payload, id):
    try:
        # params from requests
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        movie_id = body.get('movie_id')
        #
        actor = Actor.query.get(id)
        if name != None:
            actor.name = name
        if age != None:
            actor.age = age
        if gender != None:
            actor.gender = gender
        if movie_id != None:
            actor.movie_id = movie_id

        print(actor.format())
        actor.update()
        return jsonify({"success": True, "actor": actor.format()})
    except:
        abort(422)

##########################################
#   MOVIES
##########################################

#  GET movies
@app.route('/movies')
@requires_auth('get:movies')
def get_movies(payload):
    movies = []
    print("/movies")
    try:
        movie_data = Movie.query.all()
        movies = list(map(Movie.format, movie_data))
    except:
        abort(422)
    return jsonify({
        'success': True,
        'movies': movies
    })

#  POST movies
@app.route('/movies',  methods=['POST'])
@requires_auth('create:movies')
def create_movie(payload):
    try:
        # get params from request
        body = request.get_json()
        title = body.get('title')
        relese_date = body.get('relese_date')
        #
        movie = Movie(title, relese_date)
        print(movie.format())
        movie.insert()
        return jsonify({"success": True, "movie": movie.format()})
    except:
        abort(422)

#  DELETE /movies
@app.route('/movies/<id>', methods=['DELETE'])
@requires_auth('delete:movies')
def remove_movie(payload, id):
    try:
        movie = Movie.query.get(id)
        movie.delete()
        return jsonify({"success": True, "status": "deleted"})
    except:
        abort(422)

#  PATCH /movies
@app.route('/movies/<id>', methods=['PATCH'])
@requires_auth('update:movies')
def update_movie(payload, id):
    try:
        # get data from request
        body = request.get_json()
        title = body.get('title')
        relese_date = body.get('relese_date')
        #
        movie = Movie.query.get(id)
        if title != None:
            movie.title = title
        if relese_date != None:
            movie.relese_date = relese_date

        print(movie.format())
        movie.update()
        return jsonify({"success": True, "movie": movie.format()})
    except:
        abort(422)

# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

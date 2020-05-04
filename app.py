import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db, Actor, Movie
from sqlalchemy import exc
from auth.auth import AuthError, requires_auth
import json


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    return app


app = create_app()
setup_db(app)

# db_drop_and_create_all()


#  GET /actors and /movies
# * DELETE /actors/ and /movies/
# * POST /actors and /movies and
# * PATCH /actors/ and /movies/


@app.route('/', methods=['GET'])
def hello():
    return jsonify({"status": "ok"})


##########################################
#   ACTORS
##########################################

@app.route('/actors')
def get_actors():
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

@app.route('/actors', methods=['POST'])
def create_actor():
    body = request.get_json()
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')
    movie_id = body.get('movie_id')
    try:
        actor = Actor(name, age, gender, movie_id)
        print(actor.format())
        actor.insert()
        return jsonify({"success": True, "actor": actor.format()})
    except:
        abort(422)

##########################################
#   MOVIES
##########################################

@app.route('/movies')
def get_movies():
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

@app.route('/movies',  methods=['POST'])
def create_movie():
    body = request.get_json()
    title = body.get('title')
    relese_date = body.get('relese_date')
    try:
        movie = Movie(title,relese_date)
        print(movie.format())
        movie.insert()
        return jsonify({"success": True, "movie": movie.format()})
    except:
        abort(422)


# @app.route('/drinks-detail')
# @requires_auth('get:drinks-detail')
# def get_drinks_details(payload):
#     drinks = []
#     try:
#         drinks_data = Drink.query.all()
#         drinks = list(map(Drink.long, drinks_data))
#     except:
#         abort(422)
#     return jsonify({
#         'success': True,
#         'drinks': drinks
#     })


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

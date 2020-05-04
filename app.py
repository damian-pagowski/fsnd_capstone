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

@app.route('/', methods=['GET'])
def hello():
    return jsonify({"status": "ok"})

##########################################
#   ACTORS
##########################################

#  GET /actors
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

#  POST /actors
@app.route('/actors', methods=['POST'])
def create_actor():
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
def remove_actor(id):
    try:
        actor = Actor.query.get(id)
        actor.delete()
        return jsonify({"success": True, "status": "deleted"})
    except:
        abort(422)

#  PATCH /actors
@app.route('/actors/<id>', methods=['PATCH'])
def update_actor(id):
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

#  POST movies
@app.route('/movies',  methods=['POST'])
def create_movie():
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
def remove_movie(id):
    try:
        movie = Movie.query.get(id)
        movie.delete()
        return jsonify({"success": True, "status": "deleted"})
    except:
        abort(422)

#  PATCH /movies
@app.route('/movies/<id>', methods=['PATCH'])
def update_movie(id):
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

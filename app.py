import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from .database.models import db_drop_and_create_all, setup_db, Drink
from database.models import db_drop_and_create_all, setup_db, Drink
from sqlalchemy import exc
from auth.auth import AuthError, requires_auth
# from .auth.auth import AuthError, requires_auth

import json


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    return app


app = create_app()
setup_db(app)

# app.app_context().push()

db_drop_and_create_all()


@app.route('/', methods=['GET'])
def hello():
    return jsonify({"status": "ok"})


@app.route('/drinks')
def get_drinks_short():
    drinks = []
    print("ROUTE")
    try:
        drinks_data = Drink.query.all()
        drinks = list(map(Drink.short, drinks_data))
    except:
        abort(422)
    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks', methods=['POST'])
def create_drink():
    body = request.get_json()
    req_title = body.get('title')
    req_recipe = body.get('recipe')
    if not isinstance(req_recipe, list):
        abort(422)
    for each in req_recipe:
        if not('color' in each and 'parts' in each):
            abort(422)
    try:
        drink = Drink(title=req_title, recipe=json.dumps(req_recipe))
        drink.insert()
        return jsonify({"success": True, "drinks": [drink.long()]})
    except:
        abort(422)


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    drinks = []
    try:
        drinks_data = Drink.query.all()
        drinks = list(map(Drink.long, drinks_data))
    except:
        abort(422)
    return jsonify({
        'success': True,
        'drinks': drinks
    })


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

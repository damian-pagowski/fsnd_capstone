import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



port = int(os.environ.get('SERVER_PORT',3030))

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    return app


APP = create_app()


@APP.route('/', methods=['GET'])
def hello():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=port, debug=True)

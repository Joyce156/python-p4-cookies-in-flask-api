from flask import Flask, jsonify, request, session, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Secret key is required for sessions
app.secret_key = "super_secret_key"

# Database config (even if unused, keeps Flask-Migrate happy)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return {"message": "Flask Sessions & Cookies API running!"}, 200


@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):

    # Only set values if they don't already exist
    session["hello"] = session.get("hello") or "World"
    session["goodnight"] = session.get("goodnight") or "Moon"

    response = make_response(jsonify({
        'session': {
            'session_key': key,
            'session_value': session.get(key),
            'session_accessed': session.accessed,
        },
        'cookies': [
            {cookie: request.cookies[cookie]}
            for cookie in request.cookies
        ],
    }), 200)

    # Set a normal browser cookie
    response.set_cookie('mouse', 'Cookie')

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

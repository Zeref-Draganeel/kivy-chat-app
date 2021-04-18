import secrets
import time

import flask
from flask import jsonify, request

from Server.db_helper import add_user, create_message, get_message, get_messages, get_user, get_users

app = flask.Flask(__name__)
app.config["Debug"] = True

tokens = {}


class Token:
    def __init__(self, user):
        self.token = secrets.token_hex(16)
        self.expires = time.time() + 60 * 60 * 24 * 2
        self.user = user

    @property
    def expired(self):
        return time.time() > self.expires

    @expired.setter
    def expired(self, val):
        if val:
            self.expires = time.time()
        else:
            self.expires = time.time() + 60 * 60 * 24 * 2

    def __eq__(self, other):
        if isinstance(other, str):
            return self.token == other
        elif isinstance(other, Token):
            return other.token == self.token
        return False


@app.route('/signup', methods = ['POST'])
def signup():
    try:
        data = request.json
        username = data['username']
        password = data['password']
        if username in get_users():
            data = {"message": 'Username already exists'}
            return jsonify(data), 401
        add_user(username, password)
        token = Token(username)
        tokens[token.token] = token
        data = {
            "data": {
                "token": token.token,
                "expires": token.expires
            }
        }
        return jsonify(data)
    except:
        data = {"message": 'Invalid Data'}
        return jsonify(data), 401


@app.route('/login', methods = ['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']
        if get_user(username)[1] != password:
            raise
        token = Token(username)
        tokens[token.token] = token
        data = {
            "data": {
                "token": token.token,
                "expires": token.expires
            }
        }
        return jsonify(data)
    except:
        data = {"message": 'Invalid Credentials'}
        return data, 401


@app.route('/new-message', methods = ['POST'])
def new_message():
    try:
        data = request.json
        token = tokens[data['token']]
        if token.expired:
            del tokens[token.token]
            data = {"message": "Expired token"}
            return jsonify(data), 401
        message = data['message']
        create_message(token.user, message)
        data = {
            "data": {
                "message": message,
                "user": token.user
            }
        }
        return jsonify(data)
    except:
        data = {"message": 'Invalid token'}
        return jsonify(data), 401


@app.route('/messages', methods = ['GET'])
def messages():
    try:
        data = request.json
        token = tokens[data['token']]
        if token.expired:
            del tokens[token.token]
            data = {"message": "Expired token"}
            return jsonify(data), 401
        data = {
            "data": {
                "messages": get_messages(),
            }
        }
        return jsonify(data)
    except:
        data = {"message": 'Invalid token'}
        return jsonify(data), 401


@app.route('/message/<messageid>', methods = ['GET'])
def message_get(messageid):
    try:
        data = get_message(messageid)
        data = {"data": {"message": data[2], "user": data[1]}}
        return jsonify(data)
    except:
        data = {"message": 'Invalid message id'}
        return jsonify(data), 401


app.run()

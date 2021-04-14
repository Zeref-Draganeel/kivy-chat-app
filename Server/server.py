import secrets
import time

import flask
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["Debug"] = True

users = {}
tokens = []


class Token:
    def __init__(self):
        self.token = secrets.token_hex(16)
        self.expires = time.time() + 60*60*24*2

    @property
    def expired(self):
        return time.time() > self.expires

    @expired.setter
    def expired(self, val):
        if val:
            self.expires = time.time()
        else:
            self.expires = time.time()+60*60*24*2

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
        if username in users:
            data = {"message": 'Username already exists'}
            return jsonify(data), 401
        users[username] = password
        token = Token()
        tokens.append(token)
        data = {
            "message": "Created user",
            "data": {
                "token": token.token,
                "expires": token.expires
            }
        }
        return jsonify(data)
    except:
        data = {"message": 'Invalid Data'}
        return data, 401


@app.route('/login', methods = ['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']
        if users[username] != password:
            raise
        token = Token()
        tokens.append(token)
        data = {
            "message": "Logged in",
            "data": {
                "token": token.token,
                "expires": token.expires
            }
        }
        return jsonify(data)
    except:
        data = {"message": 'Invalid Credentials'}
        return data, 401


app.run()

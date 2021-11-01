#!/usr/bin/python3
# Author:	@AgbaD | @agba_dr3

import os
import pytz
import jwt
import hashlib
import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from functools import wraps

from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

CORS(app)

# admin client
a_client = FaunaClient(secret=os.getenv('FAUNA_SECRET'))

result = a_client.query(q.create_key({
    {"database": q.database("contact_validator_app"), "role": "client"}}))
client_secret = result['secret']

# server client
s_client = FaunaClient(secret=os.getenv('FAUNA_SERVER_SECRET'))

s_client.query(q.create_collection({"name": "users"}))
s_client.query(q.create_index(
    {
        "name": "users_by_username",
        "source": q.collection("users"),
        "permissions": {"read": "public"},
        "terms": [{"field": ["data", "username"]}],
        "unique": True
    }
))

s_client.query(q.create_collection({"name": "Contacts"}))
s_client.query(q.create_index(
    {
        "name": "contacts_by_id",
        "source": q.collection("Contacts"),
        "terms": [{"field": ["username", "contact", "id"]}]
    }
))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({
                'status': 'error',
                'msg': 'Access token is missing'
            }), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
            user = s_client.query(q.get(q.match(q.index("users_by_username"), data['username'])))
        except Exception:
            return jsonify({
                'status': 'error',
                'msg': 'Token is invalid'
            }), 401

        return f(user, *args, **kwargs)

    return decorated


def hash_pass(password):
    return hashlib.sha512(password.encode()).hexdigest()


@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data['username'].lower()
    password = data['password']

    try:
        user = s_client.query(
            q.get(
                q.match(q.index("users_by_username"), username)
            )
        )
        return jsonify | ({
            "msg": "error",
            "detail": "Username has been used."
        }), 400
    except:
        s_client.query(q.create(
            q.collection("users"),
            {
                "data": {
                    "username": username,
                    "password": hash_pass(password),
                    "date": datetime.now(pytz.UTC)
                },
            }
        ))
        return jsonify({
            "msg": "success",
            "detail": "Created Successfully"
        }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    try:
        user = s_client.query(
            q.get(
                q.match(q.index("users_by_username"), username)
            )
        )
        if hash_pass(password) == user["data"]["password"]:
            token = jwt.encode({
                'username': username,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], "HS256")
            return jsonify({
                'msg': 'success',
                'detail': 'Login successful',
                'data': {
                    'token': token
                }
            }), 200
        return jsonify({
            "msg": "error",
            "detail": "Password is incorrect!"
        }), 400
    except:
        return jsonify({
            "msg": "error",
            "detail": "Error! User not found"
        }), 400


@app.route("/contact/email", methods=['POST'])
def email():
    pass

# check online for tests for emails and phone numbers


if __name__ == "__main__":
    app.run()

#!/usr/bin/python3
# Author:	@AgbaD | @agba_dr3

import re
import os
import jwt
import pytz
import hashlib
from functools import wraps
from flask_cors import CORS
from faunadb import query as q
from dotenv import load_dotenv
from faunadb.client import FaunaClient
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from utils import create_server_client, parse_number

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

CORS(app)

# server client
try:
    s_client = create_server_client()
except:
    s_client = FaunaClient(secret=os.environ.get('FAUNA_SERVER_SECRET'))


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
        s_client.query(q.get(q.match(q.index("users_by_username"), username)))
        return jsonify({
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


@app.route("/validate/<email>", methods=['GET'])
@token_required
def email_val(user, email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(pattern, email):
        return jsonify({
            'msg': 'error',
            'detail': 'Email is invalid'
        }), 400
    s_client.query(q.create(
        q.collection("contacts"),
        {
            "data": {
                "contact": email,
                "username": user['data']['username'],
                "result": "valid"
            },
        }
    ))
    return jsonify({
            'msg': 'success',
            'detail': 'Email is valid'
        }), 200


@app.route("/info/<num>", methods=["GET"])
@token_required
def number(user, num):
    cond, result = parse_number(num)
    if not cond:
        try:
            if not result['valid']:
                return jsonify({
                    'msg': 'error',
                    'detail': 'Number is invalid. Please check number and try again',
                }), 400
        except:
            return jsonify({
                'msg': 'error',
                'detail': 'Could not get number info. Please check number and try again',
                'side_note': 'If this happens a couple times, best believe my free plan for the month has expired',
                'full_error': result
            }), 400

    s_client.query(q.create(
        q.collection("contacts"),
        {
            "data": {
                "contact": num,
                "username": user['data']['username'],
                "result": result
            },
        }
    ))
    return jsonify({
        'msg': 'success',
        'data': result
    }), 200


@app.route("/user/contact", methods=['GET'])
@token_required
def user_contacts(user):
    contacts = s_client.query(q.get(q.match(
        q.index("contacts_by_username"), user['data']['username']
    )))
    print(contacts)


if __name__ == "__main__":
    app.run(debug=True)

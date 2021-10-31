#!/usr/bin/python3
# Author:	@AgbaD | @agba_dr3

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

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




@app.route("/register", methods=['POST'])
def register():
	data = request.get_json()
	email = data['email']
	fullname = data['fullname']


if __name__ == "__main__":
	app.run()


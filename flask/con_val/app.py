#!/usr/bin/python3
# Author:	@AgbaD | @agba_dr3

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
CORS(app)

@app.route("/register", methods=['POST'])
def register():
	data = request.get_json()
	email = data['email']
	fullname = data['fullname']


if __name__ == "__main__":
	app.run()


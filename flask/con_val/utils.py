#!/usr/bin/python3
# Author:	@AgbaD | @agba_dr3

import os
import json
import requests
from faunadb import query as q
from faunadb.client import FaunaClient


def create_server_client():
    """
    create server client, collections and indexes
    :return: server client
    """
    client = FaunaClient(secret=os.environ.get('FAUNA_SERVER_SECRET'))

    client.query(q.create_collection({"name": "users"}))
    client.query(q.create_index(
        {
            "name": "users_by_username",
            "source": q.collection("users"),
            "permissions": {"read": "public"},
            "terms": [{"field": ["data", "username"]}],
            "unique": True
        }
    ))

    client.query(q.create_collection({"name": "contacts"}))
    client.query(q.create_index(
        {
            "name": "contacts_by_username",
            "source": q.collection("contacts"),
            "terms": [{"field": ["data", "username"]}]
        }
    ))
    return client


def parse_number(number):
    url = "http://apilayer.net/api/validate"
    params = {
        "access_key": os.environ.get("NUMVERIFY_KEY"),
        "number": number
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        return None
    resp = json.loads(resp.text)
    if not resp['valid']:
        return None
    return resp

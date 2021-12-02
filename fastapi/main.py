from fatapi import FastAPI
from typing import Optional
from faunadb import query as q
from faunadb.client import FaunaClient


app = FastAPI()

@app.get("/index")
def index(q: Optional[str] = None):
    if q:
        return {"msg": f"Welcome {q}"}
    return {"msg": "Welcome Stranger"}


# create server client

def create_server_client():

    client = FaunaClient(secret=os.environ.get('FAUNA_SECRET'))
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

    client.create_collection()
#!/usr/bin/python3

from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI
import requests
import hashlib
import jwt

app = FastAPI()

url_easy = "https://opentdb.com/api.php?amount=10&category={}&difficulty=easy"
url_medium = "https://opentdb.com/api.php?amount=10&category={}&difficulty=medium"
# Available categories:
categories = {
    "politics" : "24",
    "art" : "25",
    "history" : "23",
    "computers" : "18",
    "mathematics" : "19",
    "anime" : "31",
    "vehicles" : "28"
}


class User(BaseModel):
    name:   str
    email: str
    password: str
    current_answers: Optional[list] = None


@app.post("/login")
def login(data: User):


@app.get("/questions/{category}")
def get_questions(category: str, q: Optional[str] = "easy"):
    try:
        cat = categories[category]
    except:
        return {'status': 'error', 'details': 'Category is not valid'}

    url = url_easy
    if q != "easy":
        url = url_medium
    url = url.format(cat)
    resp = requests.get(url)


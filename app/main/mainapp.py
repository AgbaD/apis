#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

from flask import *
from flask_login import login_required, current_user

# user created
from . import main
from .. import db
from ..models import User


@main.route("/")
def index():
    return render_template('index.html')


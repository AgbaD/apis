#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

from datetime import datetime
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'user'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

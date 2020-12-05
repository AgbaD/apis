#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    admin = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.String)
    notifications = db.Colums(db.PickleType())  # dict with key of timestamp and notifications as values
    orders = db.relationship('Order', backref='user')
    transactions = db.relationship('Transaction', backref='user')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email == current_app.config['TMM_ADMIN']:
            self.admin = True

    def __repr__(self):
        return f"User(name: {fullname}, email: {email}, public_id: {public_id})"


class Order(db.Model, UserMixin):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String)  # user name + order number
    products = db.Column(db.PickleType())  # dict with key of timestamp and list of products as values
    order_id = db.Column(db.String(50), unique=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super(Orders, self).__init__(**kwargs)
        name = self.user.firstname
        self.order_name = name+' #' + self.order_id


class Product(db.Model, UserMixin):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True)
    description = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
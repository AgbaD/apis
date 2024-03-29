#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import config

moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'main.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

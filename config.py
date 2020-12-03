#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "7+/1@1m[[fvk$k@m??70[4o?aw/k4+sjhxj1%hxw[9ky2u2"
    TMM_ADMIN = os.environ.get('TMM_ADMIN') or "admin@themiddlemaan.com"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TMM_ADMIN_PASSWORD = os.environ.get('TMM_ADMIN_PASSWORD') or "12345"

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    DEBUG = True


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    TESTING = True


class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")


config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}

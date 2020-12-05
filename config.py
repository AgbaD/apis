#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "7+/1@1m[[fvk$k@m??70[4o?aw/k4+sjhxj1%hxw[9ky2u2"
    TMM_ADMIN = os.environ.get('TMM_ADMIN') or "admin@themiddlemaan.com"
    TMM_ADMIN_PASSWORD = os.environ.get('TMM_ADMIN_PASSWORD') or "fvk$k@m"
    TMM_SUPPORT = os.environ.get('TMM_SUPPORT') or "support@themiddlemaan.com"
    TMM_SUPPORT_PASSWORD = os.environ.get('TMM_SUPPORT_PASSWORD') or "o?aw/k"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_PREFIX = '[TheMiddleMaan]'

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        f"mysql+mysqlconnector://{username}:{password}@localhost/tmmdev"
    DEBUG = True


class Testing(Config):
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        f"mysql+mysqlconnector://{username}:{password}@localhost/tmmdev"
    TESTING = True


class Production(Config):
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    dbname = os.environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        f"mysql+mysqlconnector://{username}:{password}@localhost/{dbname}"


config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}

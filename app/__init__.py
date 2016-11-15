#!/usr/bin/env python
# -*- cdoing: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


db = SQLAlchemy()


def create_app(cnf):
    app = Flask(__name__)
    app.config.from_object(config[cnf])
    db.init_app(app)

    from .semd import semd
    app.register_blueprint(semd)

    return app

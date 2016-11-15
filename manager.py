#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from app import *
from flask_cors import CORS
from flask_script import Shell, Manager, Server

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
CORS(app)
# db.drop_all(app=app)
db.create_all(app=app)
manager = Manager(app)


def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))


@manager.command
def deploy():
    """Run deployment tasks."""
    pass


if __name__ == '__main__':
    manager.run()

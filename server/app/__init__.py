from flask import Flask

from .extensions import api
from .resources import ns as project_namespace

def create_app():
    app = Flask(__name__)

    api.__init__(app, doc="/")
    api.add_namespace(project_namespace)

    return app
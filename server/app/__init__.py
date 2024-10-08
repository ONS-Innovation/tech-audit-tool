from flask import Flask

from .extensions import api
from .resources import ns

def create_app():
    app = Flask(__name__)

    api.__init__(app, doc="/", title="KEH Tech Audit Tool API", version="0.1.1", description="An API that saves and accesses data from an S3 bucket in AWS saved and queried as JSON.")
    api.add_namespace(ns)

    return app
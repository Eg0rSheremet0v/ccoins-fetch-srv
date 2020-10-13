from binance.client import Client
from config import Config

from flask import Flask, Blueprint, render_template
from flask_script import Manager
from flask_restplus import Api, Namespace

import logging


app = Flask(__name__)
manager = Manager(app)
app.config.from_object(Config)

try:
    CLIENT = Client(app.config.get('API_KEY'), app.config.get('SECRET_API_KEY'))
except BaseException as ex:
    logging.exception('An error occurred while connecting to Binance API')

@app.route('/')
def base():
    return render_template("start_page.html", 
                           app_name=app.config.get('APP_NAME'),
                           app_version=app.config.get('APP_VERSION'))


blueprint = Blueprint("api", __name__, url_prefix="")

api = Api(blueprint, 
          version=app.config.get('APP_VERSION'),
          title=f"{app.config.get('APP_NAME').upper()} REST API",
          description="Application to coins management",
          doc='/docs',
          contact_email=app.config.get('APP_EMAIL'),
          validate=True)

app.register_blueprint(blueprint)

ns_base = api.namespace(f"{app.config.get('APP_NAME')}",
                        description='Base api namespace',
                        responses={
                            200: "Information about the current session was successfully received",
                            404: "Session not found"
                        })

ns_root = Namespace('Basic methods', description='Basic methods')

api.add_namespace(ns_root, ns_base.path)

from app import routes, common
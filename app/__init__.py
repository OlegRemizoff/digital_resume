from flask import Flask
from app.config import BaseConfig



def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)


    return app

app = create_app()
from app.views import *
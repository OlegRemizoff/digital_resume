from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import BaseConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    return app

app = create_app()

db = SQLAlchemy(app)
db.init_app(app)


from app.views import *






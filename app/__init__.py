from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.config import BaseConfig



def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    return app

app = create_app()

db = SQLAlchemy(app)
db.init_app(app)

from app.models import Skill
admin = Admin(app, name='Resume', template_mode='bootstrap4')
admin.add_view(ModelView(Skill, db.session, name="Навыки"))

from app.views import *






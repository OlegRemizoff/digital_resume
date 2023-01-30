from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.config import BaseConfig



def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)


from app.models import Skill
from app.views import *


### Flask-Admin
admin = Admin(app, name='Resume', template_mode='bootstrap4', index_view=DashboardView(), endpoint='admin')
admin.add_view(ModelView(Skill, db.session, name="Навыки"))









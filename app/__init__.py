from flask import Flask
from app.config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore



db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    return app


app = create_app()
from app.models import Skill, User, Role
from app.views import *


### Flask-Admin ###
admin = Admin(app, name='Resume', template_mode='bootstrap4', index_view=DashboardView(), endpoint='admin')
admin.add_view(AdminSkillView(db.session, name="Навыки"))
admin.add_view(AdminPostView(db.session, name="Блог"))
admin.add_view(ModelView(User, db.session, category="Пользователи",
               name="Пользователи", endpoint='admin/user'))
admin.add_view(ModelView(Role, db.session, name="Роль",
               category="Пользователи", endpoint='admin/post'))


### Flask-Security ###
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore) # register_form=
# user_datastore.create_user(email="", password="")
# db.session.commit()





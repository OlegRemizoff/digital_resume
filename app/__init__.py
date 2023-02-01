from flask import Flask
from app.config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_security import Security, SQLAlchemyUserDatastore





def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)


from app.models import Skill, User, Role
from app.views import *


### Flask-Admin ###
admin = Admin(app, name='Resume', template_mode='bootstrap4', index_view=DashboardView(), endpoint='admin')
admin.add_view(ModelView(Skill, db.session, name="Навыки"))
admin.add_view(ModelView(User, db.session, name="Пользователи"))
admin.add_view(ModelView(Role, db.session, name="Роль"))


### Flask-Admin ###
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)






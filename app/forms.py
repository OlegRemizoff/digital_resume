from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField
from wtforms.validators import Email, InputRequired, Length
from app import app
from app.models import Category

class PostForm(Form):
    title = StringField('Придумайте заголовок', validators=[InputRequired(), Length(min=5, max=250)])
    body = TextAreaField('Вступление', validators=[InputRequired(), Length(min=5)])
    with app.app_context():
        category = SelectField('Выберите категорию',  choices=[
            (c.id, c.name) for c in Category.query.all()], validate_choice=True)

class ContactForm(Form):
    name = StringField('Name')
    email = StringField('Email', validators=[Email()])
    message = TextAreaField('Message')

class LoginForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[Email()])
    password = PasswordField("Password")
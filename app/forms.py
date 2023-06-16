from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms.validators import Email, InputRequired, Length


class PostForm(Form):
    title = StringField('Придумайте заголовок', validators=[InputRequired(), Length(min=5, max=250)])
    body = TextAreaField('Вступление', validators=[InputRequired(), Length(min=5)])


class ContactForm(Form):
    name = StringField('Name')
    email = StringField('Email', validators=[Email()])
    message = TextAreaField('Message')

class LoginForm(Form):
    email = StringField('Email', validators=[Email()])
    password = PasswordField("Password")
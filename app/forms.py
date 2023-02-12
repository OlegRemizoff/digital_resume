from wtforms import Form, StringField, TextAreaField
from wtforms.validators import Email


class PostForm(Form):
    title = StringField('Title')
    body = TextAreaField('Body')


class ContactForm(Form):
    name = StringField('Name')
    email = StringField('Email', validators=[Email()])
    message = TextAreaField('Message')
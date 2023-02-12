from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField('Title')
    body = TextAreaField('Body')


class ContactForm():
    name = StringField('Name')
    email = StringField('Email')
    message = TextAreaField('Message')
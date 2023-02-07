from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField()
    body = TextAreaField()
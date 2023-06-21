from app import db
from flask_security import  UserMixin, RoleMixin
from sqlalchemy import DateTime
from datetime import datetime
from app.utils import slugify


class Skill(db.Model):
    # __bind_key__ = 'resume'
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    score = db.Column(db.Integer)
    position = db.Column(db.Integer)
    image = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f'skill_id: {self.id}, name: {self.name}'


### Flask-Security ###
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    image = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    last_login_at = db.Column(DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                             backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='author', lazy=True)
    def __repr__(self) -> str:
        return f'User id: {self.id}, Email: {self.email}'


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    
    def __repr__(self) -> str:
        return f'Tag id: {self.id}, Name: {self.name}'


### Blog ###
post_tags = db.Table('post_tags', 
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')) )


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String, unique=True)
    posts = db.relationship('Post', backref='category', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self) -> str:
        return f'Category id: {self.id}, Name: {self.name}'



class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer,  primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String, unique=True)  
    body = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship('Tag', secondary=post_tags,
                           backref=db.backref('post', lazy='dynamic'))
    image_preview = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    
    def __repr__(self) -> str:
            return f'Post id: {self.id}, title: {self.title}'

    def __init__(self, *args, **kwargs) -> None:
        super(Post, self).__init__(*args, **kwargs)
        self.slug = slugify(self.title)
    
    def get_date(self):
        return self.created.strftime('%d %B %Y')


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String, unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self) -> str:
        return f'Tag id: {self.id}, Name: {self.name}'
    


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f'Message id: {self.id}, Name: {self.name}'
from flask import render_template, request, url_for, redirect, flash, Markup
from app.models import Skill, Post, Message, User, Tag, Category
from app.forms import PostForm, ContactForm, LoginForm
from flask_login import login_user, logout_user, login_required
from flask_security import roles_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import  AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from sqlalchemy import desc
from app import app, db
import os

file_path = os.path.abspath(os.path.dirname(__name__))



# Админка===========================================================
#===================================================================
class DashboardView(AdminIndexView): 
	@expose('/')
	@roles_required('admin')
	def index(self):
		message = Message.query #.all()
		
		page = request.args.get("page")
		if page and page.isdigit():
			page = int(page)
		else:
			page = 1
		pages = message.paginate(page=page, per_page=5)
		return self.render('admin/dashboard.html', message=message, pages=pages)
	


	### Message delete ###
	@expose('/<int:id>/')
	@login_required
	def message_delete(self, id):
		message = Message.query.filter(Message.id==id).first()
		db.session.delete(message)
		db.session.commit()
		return self.redirect(url_for('index'))


	### Message detail ###
	# @expose('/<int:id>/')
	# @login_required
	# def message_detail(self, id):
	# 	# return "<h1>Hello: {id}</h1>"
	# 	message = Message.query.filter(Message.id==id).first()
	# 	return render_template('admin/message.html', message=message)


class AdminSkillView(ModelView):
	form_extra_fields = {
	'image': ImageUploadField(
		'',
		base_path=os.path.join(file_path, 'app/static/images/'),
		max_size=(1280, 720, True),
		thumbnail_size=(100, 100, True),
	)}

	column_labels = {
		"name": "Навык",
		"score": "Уровень",
		"position": "Позиция",
		"image": "Изображение",
	}
	column_sortable_list = ("name", "score", "position",)
	column_searchable_list = ('name',)
	create_modal = True
	edit_modal = True

	def _list_thumbnail(view, context, model, name):
		if not model.image:
			return ""
		
		url = url_for('static', filename=os.path.join('images/logo/', model.image))
		if model.image.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
			return Markup(f'<img src="{url}" width="35">')

	column_formatters =  {
		'image': _list_thumbnail	# передаем в поле image нашу функцию
	}

	def create_form(self, obj=None):
		return super().create_form(obj)
	
	def edit_form(self, obj=None):
		return super().edit_form(obj)


	def __init__(self, session,  **kwargs):
		super(AdminSkillView, self).__init__(Skill, session, **kwargs)


class AdminCategoryView(ModelView):

	column_list = (Category.id, "name", "slug", )
	column_editable_list = ("name", "slug", )
	column_labels = {
		"name": "Имя категории",
		"slug": "URL",
	}
	column_searchable_list = ('name', )
	edit_modal = True
	create_modal = True

	def create_form(self, obj=None):
		return super().create_form(obj)

	def edit_form(self, obj=None):
		return super().edit_form(obj)

	def __init__(self, session,  **kwargs):
		super(AdminCategoryView, self).__init__(Category, session, **kwargs)


class AdminPostView(ModelView):
	form_extra_fields = {
		'image_preview': ImageUploadField(
		'Изображение',
		base_path=os.path.join(file_path, 'app/static/images/post/'),
		max_size=(1500, 700, True),
		thumbnail_size=(100, 100, True),
            )}

	column_list = (Post.id, "title", "slug", "body", "created", "image_preview", )
	column_editable_list = ("title", "slug", )
	form_excluded_columns = ["image"]
	column_labels = {
		"title": "Заголовок",
		"slug": "URL",
		"body": "Текст",
		"created": "Дата создания",
		"image_preview" : "Изображение",
	}
	column_sortable_list = ('id', "title", "created",)
	column_searchable_list = ('title', 'body', )
	column_filters = ('title', 'body', 'created', )
	edit_modal = True
	create_modal = True

	def _list_thumbnail(view, context, model, name):
		if not model.image_preview:
			return ""

		url = url_for('static', filename=os.path.join('images/post/', model.image_preview))
		if model.image_preview.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
			return Markup(f'<img src="{url}" width="35">')

	column_formatters = {
		'image_preview': _list_thumbnail
	}

	def create_form(self, obj=None):
		return super().create_form(obj)

	def edit_form(self, obj=None):
		return super().edit_form(obj)

	def __init__(self, session,  **kwargs):
		super(AdminPostView, self).__init__(Post, session, **kwargs)


class AdminTagView(ModelView):

	column_list = ('id', "name", "slug", )
	column_editable_list = ("name", "slug", )
	column_labels = {
		"name": "Имя категории",
		"slug": "URL",
	}
	column_searchable_list = ('name', )
	edit_modal = True
	create_modal = True

	def create_form(self, obj=None):
		return super().create_form(obj)

	def edit_form(self, obj=None):
		return super().edit_form(obj)

	def __init__(self, session,  **kwargs):
		super(AdminTagView, self).__init__(Tag, session, **kwargs)


# Блог==============================================================
#===================================================================


### Список постов ###
@app.route('/blog/')
def blog():
	q = request.args.get('q')  # ?somethig (q, page) - попадает в args

	page = request.args.get("page")
	if page and page.isdigit():
		page = int(page)
	else:
		page = 1

	if q:
		posts = Post.query.filter(Post.title.contains(
			q) | Post.body.contains(q))  # .all()
	else:
		posts = Post.query  # .all()

	# print(request.endpoint)

	pages = posts.paginate(page=page, per_page=3)
	recent_posts = Post.query.order_by(desc(Post.created)).limit(3).all()
	tags = Tag.query.all()
	# print("\x1b[31;1m" + 'Tags' + "\x1b[0m", tags)
	print(pages)
	return render_template('blog/blog.html', posts=posts, pages=pages, tags=tags,
														recent_posts=recent_posts)


### Обзор поста ###
@app.route('/blog/post_detail/<slug>/')
def post_detail(slug):
	post = Post.query.filter(Post.slug == slug).first()
	date = post.created.strftime("%d-%m-%Y  %H:%m %p")

	context = {
		'title': post.title,
		'body': post.body,
		'date': date,
		'post': post,
		'image_preview':post.image_preview,
	}
	title = post.title

	return render_template('blog/post_detail.html', context=context, title=title)


### Посты по тегу ###
@app.route('/blog/tag/<slug>/')
def posts_by_tag(slug):

	page = request.args.get("page")
	if page and page.isdigit():
		page = int(page)
	else:
		page = 1

	tag = Tag.query.filter(Tag.slug==slug).first() # находим тег по слагу и получим связаные  посты
	posts = tag.post # .all() # благодоря backref tag получает поле post [post1, post9, ...]
	pages = posts.paginate(page=page, per_page=1)

	recent_posts = Post.query.order_by(desc(Post.created)).limit(3).all()
	tags = Tag.query.all()

	return render_template('blog/posts_by_tag.html', tag=tag, pages=pages, tags=tags,
															recent_posts=recent_posts)


### Создать пост ###
@app.route('/blog/create', methods=['GET', 'POST'])
def create_post():
	if request.method == 'POST':
		title = request.form.get('title') # form также как и args - словарь, title=название поля из форм
		body = request.form.get('body')
		
		# file = request.files['file'] # имя из формы
		# file.save(os.path.join('app/static/images/post/', file.filename))
		# image = file.filename # заносим имя файла в бд

		preview = request.files.get('preview')
		preview.save(os.path.join('app/static/images/post', preview.filename))
		image_preview = preview.filename

		try:
			post = Post(title=title, body=body,  image_preview=image_preview)
			db.session.add(post)
			db.session.commit()
		except:
			print("Something wrong!")
		return redirect(url_for('post_detail', slug=post.slug))
		
	form = PostForm()
	return render_template('blog/create_post.html', form=form)


### Редактировать пост ###
@app.route('/blog/<slug>/edit/', methods=['GET', 'POST'])
def edit_post(slug):
	post = Post.query.filter(Post.slug==slug).first()
	
	if request.method == "POST":
		preview = request.files.get('preview')
		if preview:
			preview.save(os.path.join('app/static/images/post', preview.filename))
			image_preview = preview.filename
			post.image_preview = image_preview # переопределяем изображение на полученное

			form = PostForm(formdata=request.form, obj=post) #obj - проверяет поля  на пустоту
			form.populate_obj(post,)# Заполняет атриб переданного объекта нов данными из полей формы.
			db.session.commit()
			return redirect(url_for('post_detail', slug=post.slug))
		else:
			form = PostForm(formdata=request.form, obj=post) 
			form.populate_obj(post, )
			db.session.commit()
			return redirect(url_for('post_detail', slug=post.slug))

	form = PostForm(obj=post)
	return render_template('blog/edit_post.html', post=post, form=form)



# Резюме============================================================
#===================================================================


### Список навыков ###
@app.route('/') 
def index():
    skill = Skill.query.all()
    return render_template('resume/index.html', skill=skill)


## Обратная связь ###
@app.route('/contact', methods=['GET', 'POST'])
def contact():
	if request.method == "POST":
		name = request.form['name'] # переменныe из class ContactForm()
		email = request.form['email']
		message = request.form['message']
		try:
			message = Message(name=name, email=email, message=message)
			db.session.add(message)
			db.session.commit()
			flash('The message has been sent', category="success")
		except:
			flash("Something wrong!", category="danger")
		return redirect(url_for('contact'))
		
	form = ContactForm()
	return render_template('contact.html', form=form)


### Register ###
@app.route('/register', methods=["POST", "GET"])
def register():
	form = LoginForm()		
	if request.method == "POST":
		email = request.form.get("email")
		username = request.form.get('username')
		password = request.form.get("password")
		password2 = request.form.get("password2")
		if password != password2:
			flash("Password are not equal")
			return redirect(url_for('register'))

		hash_pwd = generate_password_hash(password)
		new_user = User(email=email, username=username, password=hash_pwd, active=True)
		db.session.add(new_user)
		db.session.commit()
		flash('Register has been successfully.')
		return redirect(url_for('login'))
	
	form = LoginForm()
	return render_template('register.html', form=form)


### Log in ###
@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == "POST":
		email = request.form.get("email")
		password = request.form.get("password")
		print(email, password)

		if email and password:
			user = User.query.filter_by(email=email).first()
			if check_password_hash(user.password, password):
				login_user(user)
				flash('Logged in successfully.')
				return redirect(url_for('index'))
	
	flash("Something wrong!", category="danger")			
	form = LoginForm()
	return render_template('login.html', form=form)


### Log out ###
@app.route('/logout', methods=['POST', 'GET'])
def logout():
	logout_user()
	return redirect(url_for('index'))
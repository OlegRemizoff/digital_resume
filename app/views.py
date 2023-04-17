from flask import render_template, request, url_for, redirect, flash, Markup
from app.models import Skill, Post, Message
from app.forms import PostForm, ContactForm
from flask_admin import  AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_security import login_required
from werkzeug.utils import secure_filename
from app import app, db
import os

file_path = os.path.abspath(os.path.dirname(__name__))



### Админка ###
class DashboardView(AdminIndexView): 
	@expose('/')
	@login_required
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
		
		url = url_for('static', filename=os.path.join('images/', model.image))
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


class AdminPostView(ModelView):
	form_extra_fields = {
            'image': ImageUploadField(
		'',
		base_path=os.path.join(file_path, 'app/static/images/post/'),
		max_size=(1080, 1920, True),
		thumbnail_size=(100, 100, True),
            )}

	column_labels = {
		"title": "Заголовок",
		"slug": "URL",
		"body": "Текст",
		"created": "Дата создания",
		"image": "Изображение",
	}

	column_list = (Post.id, "title", "slug", "body", "created", "image")

	edit_modal = True
	create_modal = True

	def _list_thumbnail(view, context, model, name):
		if not model.image:
			return ""

		url = url_for('static', filename=os.path.join('images/post/', model.image))
		if model.image.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
			return Markup(f'<img src="{url}" width="35">')

	column_formatters = {
		'image': _list_thumbnail
	}

	def create_form(self, obj=None):
		return super().create_form(obj)

	def edit_form(self, obj=None):
		return super().edit_form(obj)

	def __init__(self, session,  **kwargs):
		super(AdminPostView, self).__init__(Post, session, **kwargs)


### Создать пост ###
@app.route('/blog/create', methods=['GET', 'POST'])
def create_post():
	if request.method == 'POST':
		title = request.form['title'] # form также как и args - словарь, title = название поля из форм
		body = request.form['body']
		file = request.files['file'] # имя из формы
		file.save(os.path.join('app/static/images/post/', file.filename))
		image = file.filename # заносим имя файла в бд
		try:
			post = Post(title=title, body=body, image=image)
			db.session.add(post)
			db.session.commit()
		except:
			print("Something wrong!")
		return redirect(url_for('blog'))
		
	form = PostForm()
	return render_template('blog/create_post.html', form=form)


### Редактировать пост ###
@app.route('/blog/<slug>/edit/', methods=['GET', 'POST'])
def edit_post(slug):
		post = Post.query.filter(Post.slug==slug).first()
		if request.method == "POST":
			form = PostForm(formdata=request.form, obj=post) #obj - проверяет поля  на пустоту
			form.populate_obj(post) #Заполняет атрибуты переданного объекта нов данными из полей формы.
			db.session.commit()
			return redirect(url_for('post_detail', slug=post.slug))
    	
		form = PostForm(obj=post)
		return render_template('blog/edit_post.html', post=post, form=form)


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

	pages = posts.paginate(page=page, per_page=3)

	return render_template('blog/blog.html', posts=posts, pages=pages)


### Обзор поста ###
@app.route('/blog/<slug>')
def post_detail(slug):
	post = Post.query.filter(Post.slug == slug).first()
	date = post.created.strftime("%d-%m-%Y  %H:%m %p")

	context = {
		'title': post.title,
		'body': post.body,
		'date': date,
		'post': post,
		'image':post.image,
	}
	title = post.title

	return render_template('blog/post_detail.html', context=context, title=title)


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


### Image ###
# @app.route("/upload", methods=["POST"])
# def upload_file():
# 	img = request.file['img']




# <div class="mb-3">
#   <label for="formFile" class="form-label">Пример ввода файла по умолчанию</label>
#   <input class="form-control" type="file" id="formFile">
# </div>
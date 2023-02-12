from flask import render_template, request, url_for, redirect
from app.models import Skill, Post, Message
from app.forms import PostForm, ContactForm
from flask_admin import  AdminIndexView, expose
from flask_security import login_required
from app import app, db



### Админка ###
class DashboardView(AdminIndexView): 
	@expose('/')
	@login_required
	def index(self): 
	   return self.render('admin/dashboard.html')


### Создать пост ###
@app.route('/blog/create', methods=['GET', 'POST'])
def create_post():
	if request.method == 'POST':
		title = request.form['title'] # form также как и args - словарь, title = название поля из форм
		body = request.form['body']
		try:
			post = Post(title=title, body=body)
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
		'post': post
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

		name = request.form['Name']
		email = request.form['Email']
		message = request.form['Message']
		try:
			message = Message(name=name, email=email, message=message)
			db.session.add(message)
			db.session.commit()
		except:
			print("Something wrong!")
		return redirect(url_for('contact'))

	form = ContactForm()
	return render_template('contact.html', form=form)

		
	# return render_template('contact.html')
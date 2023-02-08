from flask import render_template, request, url_for, redirect
from app.models import Skill, Post
from app.forms import PostForm
from flask_admin import  AdminIndexView, expose
from flask_security import login_required


from app import app, db



class DashboardView(AdminIndexView): 
	@expose('/')
	@login_required
	def index(self): 
	   return self.render('admin/dashboard.html')


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


@app.route('/') 
def index():
    skill = Skill.query.all()
    return render_template('resume/index.html', skill=skill)


@app.route('/blog/')
def blog():
	q = request.args.get('q')
	if q:
		posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all()	 
	else:		
		posts = Post.query.all()
	return render_template('blog/blog.html', posts=posts)


@app.route('/<slug>')
def post_detail(slug):
	post = Post.query.filter(Post.slug == slug).first()
	date = post.created.strftime("%d-%m-%Y  %H:%m %p")

	context = {
		'title': post.title,
		'body': post.body,
		'date': date,
	}
	title = post.title

	return render_template('blog/blog_detail.html', context=context, title=title)
	

	
from flask import render_template
from app.models import Skill
from flask_admin import  AdminIndexView, expose
from flask_security import login_required

from app import app





class DashboardView(AdminIndexView): 
	@expose('/')
	@login_required
	def index(self): 
	   return self.render('admin/dashboard.html')


@app.route('/') 
def index():
    skill = Skill.query.all()
    return render_template('resume/index.html', skill=skill)


@app.route('/blog/')
def blog():
	return render_template('blog/blog.html')





	
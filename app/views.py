from flask import render_template
from app.models import Skill
from flask_admin import  AdminIndexView, expose

from app import app

class DashboardView(AdminIndexView): 
	
	@expose('/') 
	def index(self): 
	   return self.render('admin/dashboard.html')


@app.route('/')
def index():
    skill = Skill.query.all()
    return render_template('resume/index.html', skill=skill)
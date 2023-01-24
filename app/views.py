from flask import render_template
from app.models import Skill

from app import app

@app.route('/')
def index():
    skill = Skill.query.all()
    return render_template('resume/index.html', skill=skill)
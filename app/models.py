from app import db

class Skill(db.Model):
    # __bind_key__ = 'resume'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    score = db.Column(db.Integer)
    position = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f'skill_id: {self.id}, name: {self.name}'
from editor.models import db

class Document(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    save_date = db.Column(db.DateTime)
    value = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


from webcheck import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from webcheck import login

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
	name = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def __repr__(self):
		return self.name

class Site(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
	title = db.Column(db.String(200), nullable=False)
	url = db.Column(db.String(200), nullable=False)

	def __repr__(self):
		return self.title + ' - ' + self.url

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
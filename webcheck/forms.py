from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])

class NewSiteForm(FlaskForm):
	title = StringField('title', validators=[DataRequired()])
	url = StringField('url', validators=[DataRequired()])
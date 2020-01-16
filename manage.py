from flask_script import Manager, Command, Option
from flask import render_template
from webcheck import app
from webcheck import db
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from webcheck.helpers import sendmail
from webcheck.helpers import test_url
import os

manager = Manager(app)
migrate = Migrate(app, db)

from webcheck.models import User, Site

@manager.command
def run():
	"""
		Runs Development Server for 
		testing purposes
	"""
	app.run()

@manager.command
def generate_secret():
	"""
		Generates a secret token for use 
		as SECRET_KEY
	"""
	secret = secrets.token_urlsafe(20)
	print(secret)

@manager.command
def collect_static():
	"""
		Collects Static Files into public folder
	"""

	public_dir = os.path.join(os.getcwd(), 'public')
	
	if os.path.isdir(public_dir):
		print('directory exists')
	else:
		os.mkdir(public_dir)

	local_static = os.path.join(os.getcwd(), 'webcheck', 'static')
	os.system("rsync -ruv --chmod=ug+w %s %s" % (local_static, public_dir))


class Email_Alert(Command):
	"""
		CLI Class to send an email alert if a site is 
		down.  python3 manage.py email_alert -t 'to@mail.com'
	"""

	def __init__(self, default_mailto='eric@rocket.farm'):
		self.default_mailto = default_mailto

	def get_options(self):
		return[
			Option('--to', '-t', dest='mailto', default=self.default_mailto)
		]

	def run(self, mailto):
		sendAlert = False
		sites = Site().query.all()
		for site in sites:
			site.status = test_url(site.url, code=True)
			if site.status is not 200:
				sendAlert = True

		if sendAlert:
			body = render_template('emails/alert_email.html', sites=sites)
			plaintext = render_template('emails/alert_email_plain.html', sites=sites)
			sendmail('launch@rocket.farm', mailto, 'Website Health Checkup', body, plaintext)
		else:
			print('All Sites Are Up')

class Add_User(Command):
	"""
		CLI class to add user to database.
		python3 manage.py -u user -p password
	"""
	
	option_list = (
		Option('--user', '-u', dest='user'),
		Option('--password', '-p', dest='password')
	)

	def run(self, user, password):
		password = generate_password_hash(password)

		user = User(name=user, password=password)
		db.session.add(user)
		db.session.commit()

		print("User: %s\nPassword: %s " % (user, password))

manager.add_command('email_alert', Email_Alert())
manager.add_command('add_user', Add_User())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()

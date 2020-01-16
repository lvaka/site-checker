from flask import Blueprint, redirect, flash, render_template, request
from webcheck.forms import LoginForm, NewSiteForm
from flask_login import current_user, login_user, logout_user
from webcheck.models import User, Site
from webcheck import db
from webcheck.decorators import login_required
from flask_json import json_response
from webcheck.helpers import jsonify_query, test_url

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
	"""
		Index Page.  Lists sites that are being
		monitored
	"""
	sites = Site().query.all()

	return render_template('index.html', sites=sites)

@main.route('/site-status')
@login_required
def site_status():
	"""
		JSON endpoint.  Test sites from 
		Database and then sends results 
		in JSON
	"""
	sites = Site().query.all()
	for site in sites:
		site.status = test_url(site.url, 200)		

	siteList = jsonify_query(sites)


	return json_response(sites=set(siteList));


@main.route('/login', methods = ['GET', 'POST'])
def login():
	"""
		Login Form.  Authenticates and logs in 
		user
	"""
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(name = form.name.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect('/login')
		
		login_user(user)
		return redirect('/')


	return render_template('login.html', form=form)

@main.route('/logout')
def logout():
	"""
		Logs out User from site
	"""
	logout_user()
	return redirect('/login')

@main.route('delete-site', methods = ['GET'])
@login_required
def delete_site():
	"""
		Deletes site. Id of site is 
		provided by GET request ID parameter
	"""
	id = request.args.get('id')
	site = Site.query.get(id)
	db.session.delete(site)
	db.session.commit()

	return redirect('/')

@main.route('/set-schedule', methods = ['GET', 'POST'])
@login_required
def set_schedule():
	"""
		Sets crontab to email 
	"""
	import os
	from pathlib import Path
	import webcheck
	from webcheck import app
	from crontab import CronTab

	user = app.config['USER']

	if request.method == 'POST':
		path = Path(os.path.dirname(webcheck.__file__)).parent
		emails = app.config['ADMIN_EMAILS']
		command = "%s/env/bin/python %s/manage.py email_alert -t %s" % (path, path, emails)

		minute = request.form['minute']
		hour = request.form['hour']
		dom = request.form['dom']
		month = request.form['month']
		dow = request.form['dow']

		cron = CronTab(user=user)
		job = ''

		commands = list(cron.find_command(command))
		
		if len(commands) < 1:
			job = cron.new(command=command)
			job.setall(minute, hour, dom, month, dow)
		else:
			job = commands[0]
			job.setall(minute, hour, dom, month, dow)

		cron.write() if job.is_valid() else print('not valid job')

		return redirect('/')

	return render_template('schedule_cron.html')

@main.route('/clear-schedule')
@login_required
def clear_schedule():
	"""
		Clears job from cron
	"""
	import os
	from pathlib import Path
	import webcheck
	from webcheck import app
	from crontab import CronTab

	user = app.config['USER']
	path = Path(os.path.dirname(webcheck.__file__)).parent
	command = "python %s/manage.py email_alert -t eric@rocket.farm" % path
	cron = CronTab(user=user)
	commands = list(cron.find_command(command))

	if len(commands):
		job = commands[0]
		cron.remove( job )
		cron.write()

	return redirect('/')


@main.route('/new-site', methods = ['GET', 'POST'])
@login_required
def newsite():
	"""
		Form for adding new site to 
		Database to check
	"""
	form = NewSiteForm()

	if form.validate_on_submit():
		title = form.title.data
		url = form.url.data
		site = Site(title=title, url=url)
		db.session.add(site)
		db.session.commit()

		return redirect('/')

	return render_template('new_site_form.html', form=form)
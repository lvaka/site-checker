import json
import requests
import os

def jsonify_query(query):
	jsonList = []
	for item in query:
		itemDict = item.__dict__.copy()
		del itemDict['_sa_instance_state']
			
		jsonList.append(json.dumps(itemDict))

	return jsonList

def test_url(url, status=200, code=False):
	test = '';

	try:
		res = requests.get(url)
		if(code):
			test = res.status_code
		else:
			test = res.status_code == status
	except:
		if(code):
			test = 504
		else:
			test = False

	return test

def sendmail(email_from, email_to, email_subject, email_body, plaintext):
	"""
		Generates an e-mail and sends through system's sendmail command
	"""
	from webcheck import app
	sendmail_location = app.config['SENDMAIL_LOCATION']
	
	email_to = ', '.join(email_to) if isinstance(email_to, list) else email_to
	sendmail = os.popen("%s -t" % sendmail_location, 'w')
	sendmail.write("From: %s\n" % email_from)
	sendmail.write("To: %s\n" % email_to)
	sendmail.write("Mime-Version: 1.0\n")
	sendmail.write("Content-Type: multipart/alternative; boundary=bounds\n")
	sendmail.write("Subject: %s\n" % email_subject)
	sendmail.write("\n")
	sendmail.write("--bounds\n")
	sendmail.write("Content-Type: text/plain; charset=utf-8\n\n")
	sendmail.write(plaintext)
	sendmail.write("\n\n")
	sendmail.write("--bounds\n")
	sendmail.write("Content-Type: text/html; charset=utf-8\n\n")
	sendmail.write(email_body)
	sendmail.write("\n")
	sendmail.write("--bounds\n")
	sendmail.close()
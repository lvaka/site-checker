# Site-Down Detector

A simple Flask based web app that lets me monitor client sites up time.

Sites are stored in a database by title and url.  Each site is sent a get request using the default Python requests library.

The front facing site has a manual test function that will return whether or not each site returns a 200 status request.

In addition to the manual test button, you can set a schedule in cron.  Cron will call a command line script from the manage.py module, run tests, and write an email to Admins.

## Command Line Interface

Migrations are handled through Flask CLI on manage.py.  You can run init, migrate, and upgrade.  ie "python manage.py db init, python manage.py db migrate, python manage.py db upgrade".

**Other cli commands**
* email_alert -t *emailto* | sends an email with site check if there's a non 200 response code
* add_user -u *username* -p *password* | adds an authorized user for the site checker site
* collect_static | collects static files to public folder
* generate_secret | generates a hash code
* run | runs an http server for testing

## Config
To run, variables need to be set in config.py.  Use config.py.example as a template to set your own environmental variables for the app.

## Front End
Bootstrap 4 is used to style the front end.  Axios is used to make AJAX calls.  Webpack is set up to compile sass and javascript and minify for production
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_json import FlaskJSON

db = SQLAlchemy()
csrf = CSRFProtect()
login = LoginManager()
json = FlaskJSON()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
csrf.init_app(app)
db.init_app(app)
login.init_app(app)
json.init_app(app)

from webcheck.controllers import main


app.register_blueprint(controllers.main, url_prefix="/")
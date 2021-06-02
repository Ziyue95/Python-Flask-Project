# -*- encoding=UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.jinja_env.add_extension("jinja2.ext.loopcontrols")# add loopcontrol extension of jinja environment to support break in loop
app.config.from_pyfile("app.conf")#directly import configure file from here
app.secret_key = 'nowcoder'
db = SQLAlchemy(app)
login_manager = LoginManager(app)#initialte login manager from flask-login package
login_manager.login_view = "/regloginpage/"#set login page to "/regloginpage/"

from nowstagram import views,models
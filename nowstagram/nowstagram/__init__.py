# -*- encoding=UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.add_extension("jinja2.ext.loopcontrols")# add loopcontrol extension of jinja environment to support break in loop
app.config.from_pyfile("app.conf")#directly import configure file from here
app.secret_key = 'nowcoder'
db = SQLAlchemy(app)

from nowstagram import views,models
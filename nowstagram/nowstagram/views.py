# -*- encoding=UTF-8 -*-

from nowstagram import app
from nowstagram import db
from nowstagram.models import User,Image
from flask import render_template,redirect,request,flash,get_flashed_messages
import random, hashlib

@app.route("/")#homepage
def index():
    # List image based on user id in a descending order
    images = Image.query.order_by(Image.id.desc()).limit(10).all()
    return(render_template("index.html",images = images))

@app.route("/image/<int:image_id>/")
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect("/")
    return render_template("pageDetail.html",image = image)

@app.route("/profile/<int:user_id>/")
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect("/")
    return render_template("profile.html",user = user)

@app.route("/regloginpage/")
def regloginpage():
    msg = ""
    for m in get_flashed_messages(with_categories=False, category_filter=["reglogin"]):
        msg = msg + m
    return render_template("login.html",msg = msg)

def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)

@app.route("/reg/", methods={"post","get"})
def reg():
    #requst.args
    #request.form
    username = request.values.get("username").strip()#strip() ignore space before/after username
    password = request.values.get("password").strip()

    if username == "" or password == "":
    #if not username or not password:
        return redirect_with_msg("/regloginpage/", u"Your username or password is invalid", category="reglogin")

    user = User.query.filter_by(username=username).first()
    if user != None:
        return redirect_with_msg("/regloginpage/",u"Pilot Account has already been registered", category="reglogin")

    #More checks

    salt = ".".join(random.sample("01234567890abcdefghiABCDEFGHIJKLMNOPQRST",10))
    m = hashlib.md5() #setup a md5 encryption
    #m.update(password+salt) #add salt
    salted_password = password+salt
    m.update(salted_password.encode('utf-8'))
    password = m.hexdigest()
    user = User(username,password,salt)
    db.session.add(user)
    db.session.commit()

    return redirect("/")
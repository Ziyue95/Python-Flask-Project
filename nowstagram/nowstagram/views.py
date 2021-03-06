# -*- encoding=UTF-8 -*-
import uuid

from nowstagram import app
from nowstagram import db
from nowstagram.models import User,Image, Comment
from flask import render_template,redirect,request,flash,get_flashed_messages, send_from_directory
import random, hashlib, json, uuid, os
from flask_login import login_user, logout_user, current_user, login_required
from nowstagram.qiniusdk import qiniu_upload_file

@app.route("/")#homepage
def index():
    # List image based on user id in a descending order
    images = Image.query.order_by(Image.id.desc()).limit(10).all()
    return(render_template("index.html",images = images))
    #user = User.query.all()
    #paginate = Image.query.order_by(Image.id.desc()).paginate(page=1, per_page=5, error_out=False)
    #return render_template("index.html", images = paginate.items, has_next=paginate.has_next)

@app.route('/index/images/<int:page>/<int:per_page>/')
def index_images(page, per_page):
    paginate = Image.query.order_by(db.desc(Image.id)).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        comments = []
        for i in range(0, min(2, len(image.comments))):
            comment = image.comments[i]
            comments.append({'username':comment.user.username,
                             'user_id':comment.user_id,
                             'content':comment.content})
        imgvo = {'id': image.id,
                 'url': image.url,
                 'comment_count': len(image.comments),
                 'user_id': image.user_id,
                 'head_url':image.user.head_url,
                 'created_date':str(image.created_date),
                 'comments':comments}
        images.append(imgvo)

    map['images'] = images
    return json.dumps(map)

@app.route('/image/<int:image_id>/')
@login_required
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect('/')
    comments = Comment.query.filter_by(image_id=image_id).order_by(db.desc(Comment.id)).limit(20).all()
    return render_template('pageDetail.html', image=image, comments=comments)


@app.route("/profile/<int:user_id>/")
@login_required #require login status; unloigined visit will be blocked
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect("/")
    #divide images into different pages
    paginate = Image.query.filter_by(user_id = user_id).paginate(page=1, per_page=3, error_out=False)
    return render_template("profile.html",user = user, images=paginate.items, has_next=paginate.has_next)

@app.route("/profile/images/<int:user_id>/<int:page>/<int:per_page>/")
def user_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    map = {"has_next": paginate.has_next}
    images = []
    for image in paginate.items:
        imgvo = {"id":image.id, "url":image.url, "comment_count":len(image.comments)}#imgvo stores the json attributes for each image
        images.append(imgvo)
    map["images"] = images
    return json.dumps(map)#output json file

@app.route("/regloginpage/")
def regloginpage():
    msg = ""
    for m in get_flashed_messages(with_categories=False, category_filter=["reglogin"]):
        msg = msg + m
    return render_template("login.html",msg = msg, next = request.values.get("next"))#fetch information on "next" from request method, and set value to next

def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)

@app.route("/login/", methods={"post","get"})
def login():
    username = request.values.get("username").strip()#strip() ignore space before/after username
    password = request.values.get("password").strip()

    if username == "" or password == "":
        # if not username or not password:
        return redirect_with_msg("/regloginpage/", u"Your username or password is invalid", category="reglogin")

    user = User.query.filter_by(username=username).first()
    if user == None:
        return redirect_with_msg("/regloginpage/", u"Username does not exist", category="reglogin")
    m = hashlib.md5() #setup a md5 encryption
    salted_password = password + user.salt
    m.update(salted_password.encode('utf-8'))
    if (m.hexdigest() != user.password):
        return redirect_with_msg("/regloginpage/", u"Password incorrect", category="reglogin")

    login_user(user)
    next = request.values.get("next")#check the value of next
    if next != None and next.startswith("/"):
        return redirect(next)


    return redirect("/")

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

    login_user(user)

    next = request.values.get("next")  # check the value of next
    if next != None and next.startswith("/"):
        return redirect(next)

    return redirect("/")

@app.route("/logout/")# setup logout, then redirect to homepage
def logout():
    logout_user()
    return redirect("/")

def save_to_local(file, file_name):#upload and save
    save_dir = app.config["UPLOAD_DIR"]
    file.save(os.path.join(save_dir,file_name))
    return "/image/" + file_name

@app.route("/image/<image_name>")
def view_image(image_name):
    return send_from_directory(app.config["UPLOAD_DIR"], image_name)

def save_to_qiniu(file, file_name):
    return qiniu_upload_file(file, file_name)

def save_to_local(file, file_name):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, file_name))
    return '/image/' + file_name

@app.route('/upload/', methods={"post"})
@login_required
def upload():
    file = request.files['file']
    # http://werkzeug.pocoo.org/docs/0.10/datastructures/
    # ????????????????????????????????????
    file_ext = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        url = qiniu_upload_file(file, file_name)
        #url = save_to_local(file, file_name)
        if url != None:
            db.session.add(Image(url, current_user.id))
            db.session.commit()

    return redirect('/profile/%d' % current_user.id)

@app.route("/addcomment/",methods={"post"})
def add_comment():
    image_id = int(request.values["image_id"])
    content = request.values["content"]
    comment = Comment(content,image,current_user.id)
    db.session.add(comment)
    db.session.commit()
    return json.dumps({"code":0,"id":comment.id,
                       "content":content,
                       "username":comment.user.username,
                       "user_id":comment.user.id})


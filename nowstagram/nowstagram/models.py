# -*- encoding=UTF-8 -*-

from nowstagram import db, login_manager
from datetime import datetime
import random

class Comment(db.Model):#connect to database create database image
    # set id,url,user_id,created_data as columns in this database
    #__tablename__ = "MyComment" # Change the name of database table to MyCooment
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    image_id = db.Column(db.Integer, db.ForeignKey("image.id"))#ForeignKey mean this key value is from other database, here from table image with column id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    status = db.Column(db.Integer, default= 0) #0 is normal 1 is deleted, defaul is 0
    user = db.relationship("User")# use relationship function to relate this attribute to other database, here User

    def __init__(self,content,image_id,user_id):
        self.content = content
        self.image_id = image_id
        self.user_id = user_id

    def __repr__(self): #__repr__ is a special method used to represent a class’s objects
        return "<Comment %d %s>" %(self.id, self.content) #Syntax: object.__repr__(self) Returns a string as a representation of the object.

class Image(db.Model):#connect to database create database image
    # set id,url,user_id,created_data as columns in this database
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))#ForeignKey mean this key value is from other database, here from database user with column id
    created_date = db.Column(db.DateTime)
    comments = db.relationship("Comment")

    def __init__(self,url,user_id):
        self.url = url
        self.user_id = user_id
        self.created_date = datetime.now() #this will return the current datetime

    def __repr__(self): #__repr__ is a special method used to represent a class’s objects
        return "<Image %d %s>" %(self.user_id, self.url) #Syntax: object.__repr__(self) Returns a string as a representation of the object.

class User(db.Model):#connect to database create database user
    #__tablename__ = "xuser" # Change the name of table to xuser
    # set id,username,password,head_url as columns in this database
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80), unique=True) #username becomes one column in the database
    password = db.Column(db.String(32))
    salt = db.Column(db.String(32))
    head_url = db.Column(db.String(256))
    images = db.relationship("Image", backref="user", lazy="dynamic")# use relationship function to relate this attribute to other database, here Image
                                                                     # use backref to allow image refer back to user;

    def __init__(self,username,password,salt=""):
        self.username = username
        self.password = password
        self.salt = salt
        self.head_url = "https://images.nowcoder.com/head/"+ str(random.randint(0,1000)) +"m.png"

    def __repr__(self): #__repr__ is a special method used to represent a class’s objects
        return "<User %d %s>" %(self.id, self.username) #Syntax: object.__repr__(self) Returns a string as a representation of the object.
    # Add more properties and methods from flask-login to enable user login/logout
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True


    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)#query user id from database

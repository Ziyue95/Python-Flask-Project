# -*- encoding=UTF-8 -*-

from nowstagram import app,db
from flask_script import Manager
from sqlalchemy import or_,and_
from nowstagram.models import User,Image, Comment #import different class if object from models
import random

manager = Manager(app)

def get_image_url():
    return "https://images.nowcoder.com/head/"+ str(random.randint(0,1000)) +"m.png"

@manager.command
def init_database():
    #delete two lines below, then we will not always first initializa new database
    db.drop_all() #drop everything in the database
    #db here refers to the metadata of one type of table
    db.create_all() #create the new database contained all defined variables
    for i in range(100):
        db.session.add(User("User" + str(i+1), "a" + str(i)))#add 100 new users, object in class User has 2 attributes "username" and ”password“ as defined in models.py
        for j in range(3):
            db.session.add(Image(get_image_url(),i+1))#add 3 images for each user, object in class Image has 2 attributes "url" and ”user_id“ as defined in models.py
            for k in range(3):
                db.session.add(Comment("This is the " + str(k+1) + "th comment on " + str(1+3*i+j) + "th image, written by " + str(1+i) + "th User.", 1+3*i+j, i+1))
    for j in range(5):
        db.session.add(Image(get_image_url(), 100))

    db.session.commit() #Commit all pending changes to database

    for i in range(50,100,2):
        user = User.query.get(i) # First way to update item
        user.username = "[New1]" + user.username

        user = User.query.get(i+1) # Second way to update item
        User.query.filter_by(id=i+1).update({"username":"[New2]" + user.username})
    db.session.commit()

    #Delete items from table
    #for i in range(50, 100, 2): # First way to delete item
    #    comment = Comment.query.get(i+1)
    #    db.session.delete(comment)
    #Comment.query.filter_by(id = 10).delete()# Second way to delete item

    db.session.commit()


    """
    print(Mycomment.__tablename__)
    print(User.__tablename__)
    """
    print(1, User.query.all()[0:3])  # print the representation of class object <-defined in __rep__(self)
    print(2, User.query.get(3)) # print the representation of 3rd object in table user
    print(3, User.query.filter_by(id = 5).first()) # use filter when doing queries
    print(4, User.query.order_by(User.id.desc()).limit(3).all()) #desc(): In descending order; aesc(): In ascending order;
    print(5, User.query.order_by(User.id.asc()).offset(1).limit(2).all()) # Offset by 1, limit by 2
    print(6, User.query.filter(User.username.endswith("0")).limit(3).all()) # print all users whose username ends with "0"
    print(7, User.query.filter(or_(User.id == 88 , User.id == 99)).all()) # use or in filter
    print(8, User.query.filter(or_(User.id == 88, User.id == 99))) # Print the select command in sql
    print(9, User.query.filter(and_(User.id > 88, User.id < 92)).all()) # use and in filter
    print(10, User.query.filter(and_(User.id > 90, User.id < 92)).first_or_404()) # print first id if possible otherwise raise 404 error
    print(11, User.query.filter(and_(User.id > 100, User.id < 92)).first())  # use first not first_or_404, will return None if it can not find any objects
    print(12, User.query.paginate(page = 3, per_page=4).items) #seperate page using pagonate, and return 3rd page where each page contains 4 objects
    print(13, User.query.order_by(User.id.desc()).paginate(page=3, per_page=4).items)  # seperate page using pagonate, reverse by the id first
    print(14, User.query.filter(and_(User.id > 50, User.id % 2 == 1)).limit(5).all())
    print(15, user.images) # One-to-Many Relationship: since one user is related to 3 images; This is done by 1.images = db.relationship("Image"); 2.user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    for i in range(2):
        image = Image.query.get(4)
        print(16, image, image.user,image.created_data)
    print(17, User.query.all())





if __name__ == "__main__":
    manager.run()
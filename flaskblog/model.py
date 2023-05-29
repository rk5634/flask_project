from flaskblog import db,login
from datetime import datetime,timedelta
from flask_login import UserMixin
import jwt
import os

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    firstname = db.Column(db.String(20),nullable = False)
    lastname = db.Column(db.String(20),nullable = False,default = "")
    username = db.Column(db.String(20),unique = True,nullable = False)
    email = db.Column(db.String(120),unique = True,nullable = False)
    image_file = db.Column(db.String(20),nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60),nullable = False)
    posts = db.relationship("Post",backref = "author",lazy = True)

    def get_reset_token(self,exp_time=30):
        x = jwt.encode({"user_id":self.id,
                        "exp":int((datetime.now()+timedelta(seconds=exp_time)).timestamp())},
                        os.environ.get('SECRET_KEY'),
                        algorithm="HS256")
        return x
    
    @staticmethod
    def verify_reset_token(token):
        try:
            d = jwt.decode(token,os.environ.get("SECRET_KEY"),algorithms="HS256")
        except:
            return None
        return User.query.get(d['user_id'])


    def __repr__(self):
        return f'{self.firstname}, {self.lastname}, {self.username}, {self.email}, {self.image_file}'
    


class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    date_posted = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)
    content = db.Column(db.Text,nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    def __repr__(self):
        return f"title = {self.title}, date_posted = {self.date_posted}"
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField , SubmitField,BooleanField
from wtforms.validators import data_required,length,Email,EqualTo,ValidationError
from flaskblog.model import User

def validate_username(self,username):
        if current_user.is_authenticated and username.data == current_user.username:
            return
        user = User.query.filter_by(username = username.data).first()
        if(user):
            raise ValidationError("Username already exists")
        
def validate_email(self,email):
    if current_user.is_authenticated and email.data == current_user.email:
        return
    user = User.query.filter_by(email = email.data).first()
    if(user):
        raise ValidationError("Email already exists")
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',validators=[data_required(),length(min=2,max=20)])
    lastname = StringField('Last Name',validators=[length(min=0,max=20)])
    username = StringField('Username',validators=[data_required(),length(min=2,max=10),validate_username])
    email = StringField('Email',validators=[data_required(),Email(),validate_email])
    password = StringField('Password',validators=[data_required(),length(min=8,max=20)])
    confirm_password = StringField('Confirm Password',validators=[data_required(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    
        

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[data_required(),Email()])
    password = StringField('Password',validators=[data_required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    firstname = StringField('First Name',validators=[data_required(),length(min=2,max=20)])
    lastname = StringField('Last Name',validators=[length(min=0,max=20)])
    username = StringField('Username',validators=[data_required(),length(min=2,max=10),validate_username])
    email = StringField('Email',validators=[data_required(),Email(),validate_email])
    image = FileField('Profile Picture',validators=[FileAllowed(['jpg','png'])])
    update = SubmitField('Update')
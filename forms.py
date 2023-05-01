from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField,BooleanField
from wtforms.validators import data_required,length,Email,EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[data_required(),length(min=2,max=10)])
    email = StringField('Email',validators=[data_required(),Email()])
    password = StringField('Password',validators=[data_required(),length(min=8,max=20)])
    confirm_password = StringField('Confirm Password',validators=[data_required(),EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[data_required(),Email()])
    password = StringField('Password',validators=[data_required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
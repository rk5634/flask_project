from flask import Flask,render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm
from model import User,Post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f8285140719d033ac7230676f0afeaf2'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)




p = [
    {
    'author':"RK1",
    'title':"Blog 1",
    'content':'First Post Content',
    'date':'April 7, 2023'
    },
    {
    'author':"RK2",
    'title':"Blog 2",
    'content':'Second Post Content',
    'date':'April 8, 2023'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",post=p)

@app.route("/about")
def about():
    return render_template("about.html",title = "About Page")


@app.route("/register",methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title = 'Register',form = form)

@app.route("/login",methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "heythisisrk@gmail.com" and form.password.data == "password":
            flash("You have logged in successfully !","alert alert-primary alert")
            return redirect(url_for('home'))
        else:
            flash("Login Failed !!",'danger')

    return render_template('login.html',title = 'Login',form = form)

@app.route("/rk")
def rk():
    return "ALTAIR hello"
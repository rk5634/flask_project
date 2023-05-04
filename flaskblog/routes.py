from flask import render_template,url_for,flash,redirect,request
from flaskblog.forms import RegistrationForm,LoginForm
from flaskblog.model import User,Post
from flaskblog import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data,email = form.email.data,password = hash_password,firstname = form.firstname.data,lastname = form.lastname.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for you can login now!','success')
        return redirect(url_for('login'))
    else:
        pass
        

    return render_template('register.html',title = 'Register',form = form)

@app.route("/login",methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else  redirect(url_for('home'))
        else:
            flash("Login Failed !!",'danger')

    return render_template('login.html',title = 'Login',form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html',title = 'Account')

@app.route("/models")
@login_required
def models():
    return render_template('models.html',title = "Models")


@app.route("/rk")
def rk():
    return "ALTAIR hello"
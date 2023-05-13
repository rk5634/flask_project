import secrets
import os
from PIL import Image
from flask import render_template,url_for,flash,redirect,request,abort
from flaskblog.forms import RegistrationForm,LoginForm,UpdateProfileForm,CreatePostForm,EditPostForm
from flaskblog.model import User,Post
from flaskblog import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required




@app.route("/")
@app.route("/home")
def home():
    p = Post.query.all()
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
    image_file = url_for('static',filename = f'profile_pics/{current_user.image_file}')
    return render_template('account.html',title = 'Account',image_file = image_file)

@app.route("/models")
@login_required
def models():
    return render_template('models.html',title = "Models")




def saveimage(formimage):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(formimage.filename)
    image_fn = random_hex+f_ext
    image_path = os.path.join(app.root_path,'static/profile_pics',image_fn)

    output_size = (125,125)
    i = Image.open(formimage)
    i.thumbnail(output_size)
    i.save(image_path)
    return image_fn 
    
@app.route('/account/update_profile',methods = ['GET','POST'])
@login_required
def update_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = saveimage(form.image.data)
            current_user.image_file = image_file
        user = User.query.filter_by(username = current_user.username).first()
        user.email = form.email.data
        user.username = form.username.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        db.session.commit()
        flash('Your profile is updated!','success')
        return redirect(url_for('account'))
    
    elif request.method=='GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data  = current_user.email
    return render_template('updateprofile.html',form = form)



@app.route("/create_post",methods = ['GET','POST'])
@login_required
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data,content = form.content.data,user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("New Post Created")
        return redirect(url_for("home"))
    return render_template("new_post.html",form=form,title="New Post")


@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html",post = post,title = post.title)

@app.route("/post/<int:post_id>/edit_post",methods = ["POST","GET"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if(current_user.id != post.author.id):
        abort(403)
    form = EditPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Updated")
        return redirect(url_for("home"))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("edit_post.html",post = post,form =form,title = "Edit Post")

@app.route("/post/<int:post_id>/delete_post",methods = ["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.author.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!")
    return redirect(url_for('home'))
@app.route("/rk")
def rk():
    return "ALTAIR hello"
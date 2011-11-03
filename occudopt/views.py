from flask import Flask
from flask import request, url_for, render_template, flash, redirect
from occudopt import app
from models import User, Image, Relationship, OccupyCity, Message
from flaskext.mongoengine.wtf import model_form
from flaskext.mongoengine import MongoEngine
from flaskext.login import LoginManager, login_user, logout_user, login_required, current_user
from flaskext import uploads
from flaskext.uploads import IMAGES, configure_uploads, patch_request_class


#flask-uploads init
photos = uploads.UploadSet('photos', IMAGES)
configure_uploads(app, (photos))
patch_request_class(app, 2 * 1024 * 1024) #2mb upload max


#flask-login init
login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(email):
	#load user, return id
	return User.objects(email=email)[0]

#Let 'er rip!
@app.route("/user/login", methods=["GET", "POST"])
def login():
	import bcrypt
	PostForm = model_form(User)
	form = PostForm(request.form)
	if request.method == 'POST': #and form.validate():
		email = request.form['email']
		password = request.form['password'] # the password as entered in the form
		u = User.objects(email=email)[0]
		hashed = u.password # the stored, hashed password
		# login and validate the user...
		if bcrypt.hashpw(password, hashed) == hashed:
				login_user(u)
				flash("Logged in successfully.")
				return redirect(request.args.get("next") or url_for("logged_in"))
		else:
				return "password does not match email"
	return render_template("login.html", form=form)
	
@app.route('/user/logged_in')
@login_required
def logged_in():
	return "Urine!"
	
@app.route("/user/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("index"))

@app.route("/user/all")
def list_all_users():
	return render_template('all_users.html', users = User.objects().all())

@app.route("/user/unadopted")
def list_unadopted_users():
	u = User.objects(adopted_by__size = 0)
	return render_template('unadopted_users.html', users = u)

@app.route('/')
def index():
	num_users = User.objects().count()
	if current_user.is_authenticated(): 
		user = str(current_user.first_name + " " + current_user.last_name) 
		return '%d active users ' % num_users + ' ' + "</br>Welcome, " + user + "." + "</br><a href = " + url_for("logout") +">Log out</a>"
	else: 
		user = "anonymous"
		return "Welcome to OccuDopt.  <a href=" + url_for("login") + ">Log In</a>"
	
@app.route('/user/profile/<email>')
	def user_profile(email):
		u = User.objects(email = email)
		return "okay"
		#return render_template('user_profile.html', user = u)
		
#TODO add check against existing email
@app.route('/user/add/', methods=['GET', 'POST'])
def user_add():
	import bcrypt
	PostForm = model_form(User)
	form = PostForm(request.form)
	if request.method == 'POST': #and form.validate():
		#the following is described in flask-uploads documentation
		filename = "" #store blank photo filename
		#initialize default user photo
		i = Image(image_path = 'default_image', is_profile=True) 
		if 'photo' in request.files:
			filename = photos.save(request.files['photo'])
			i = Image(image_path = filename, is_profile=True)
			flash("Photo saved.")
		i.save()
		#hash password stored in database so that it is not viewable by people in Romania
		hashed = bcrypt.hashpw(request.form["password"], bcrypt.gensalt())
		u = User(	email = request.form["email"], 
					first_name = request.form["first_name"], 
					last_name =request.form["last_name"], 
					password = hashed, 
					authenticated = False,
					philosophy = request.form['philosophy'],
					tags = request.form['tags'].split(','),
				)
		u.profile_picture= i
		u.save()
		return "done:" + request.form["email"] + " " + request.form["first_name"]+ " " + request.form["last_name"] + " " + '/_uploads/photos/'+i.image_path
	else:
		return render_template('add.html', form=form, cities = OccupyCity.objects.all())

@app.route('/photo/<email>')
def photo_from_email(email):
	u = User.objects(email = email)
	photo = u[0].profile_picture
	if photo is None:
		abort(404)
	url = photos.url(photo.image_path)
	return url 
	#return render_template('show.html', url=url, photo=photo)

@app.route('/user/remove/', methods=['GET', 'POST'])
def user_remove():
	return "blah"
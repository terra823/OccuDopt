from flask import Flask
from flask import request, url_for, render_template
from flaskext.mongoengine import MongoEngine
from flaskext.mongoengine.wtf import model_form


app = Flask(__name__)
app.config.from_pyfile('config.py')
#app.config['MONGODB_DB'] = 'testing'
db = MongoEngine(app)

class User(db.Document):
	email = db.StringField(required = True)
	first_name = db.StringField(max_length = 50)
	last_name = db.StringField(max_length = 50) 
	
PostForm = model_form(User)

@app.route('/')
def showdata():
	num_users = User.objects().count()
	return ('Found %d users ' % num_users)

@app.route('/user', methods=['GET', 'POST'])
def add_post():
	form = PostForm(request.form)
	if request.method == 'POST': #and form.validate():
	# do something
		u = User(email = request.form["email"], first_name = request.form["first_name"], last_name =request.form["last_name"])
		u.save()
		return "done:" + request.form["email"] + " " + request.form["first_name"]+ " " + request.form["last_name"]
	else:
		return render_template('add.html', form=form)



if __name__ == '__main__':
	app.run(debug=True)
	

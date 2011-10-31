from flask import Flask
from flask import request, url_for, render_template
from flaskext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_pyfile('config.py')
#app.config['MONGODB_DB'] = 'testing'
db = MongoEngine(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)


    

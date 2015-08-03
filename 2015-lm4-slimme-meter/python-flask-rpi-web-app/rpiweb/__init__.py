'''
Created on Dec 28, 2013

@author: hugo
'''

from flask import Flask
from .models import db
from .routes import rpiapp

# set up the flask app
app = Flask(__name__)  
app.config.from_object('config')

# map db to app
db.init_app(app)

# use blueprints
app.register_blueprint(rpiapp)
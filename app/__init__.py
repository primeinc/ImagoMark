import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imago_mark.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.abspath('instance/uploads')
app.config['THUMBNAIL_FOLDER'] = os.path.abspath('instance/thumbnails')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
  os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['THUMBNAIL_FOLDER']):
  os.makedirs(app.config['THUMBNAIL_FOLDER'])

db = SQLAlchemy(app)

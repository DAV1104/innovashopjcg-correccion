from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

import pymysql

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3307/incjg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "0febc2ce4e68016ccf8bc4fd8b9687b9"

db = SQLAlchemy(app)
ma = Marshmallow(app)    
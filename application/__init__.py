from flask import Flask,Blueprint,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_marshmallow import Marshmallow

from flask_mail import Mail, Message
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asjd9792nasd887a8dA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/nux'

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'admin.Login'

ma= Marshmallow(app)
from application.Main.routes import main
app.register_blueprint(main)

from application.Admin_Panel.routes import admin
app.register_blueprint(admin)




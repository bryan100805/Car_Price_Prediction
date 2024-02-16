from flask import Flask, current_app
from flask_mail import Mail
import pickle
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#instantiate SQL Alchemy to handle db process
db =SQLAlchemy()

#create the Flask app
app = Flask(__name__) 

#instantiate Bcrypt to handle password hashing
bcrypt = Bcrypt(app)

#instantiates login manager to handle user login
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login_page'

# Initiate mail to handle email sending
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "daaa2b01.2214449.tanwentaobryan@gmail.com"
app.config["MAIL_PASSWORD"] = "sqhrubshwgeueige"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

# instantiate mail to handle email sending
mail = Mail(app)

# load configuration from config.cfg
app.config.from_pyfile('config.cfg') 

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# new method for SQLAlchemy version 3 onwards
with app.app_context():
    db.init_app(app) 
    from .models import Entry
    db.create_all()
    db.session.commit()
    print('Created Database!')

#AI model file
joblib_file = "./application/static/carPrice_GBModel.pkl"
# Load from file
with open(joblib_file, 'rb') as f: 
    ai_model = pickle.load(f) 

#run the file routes.py
from application import routes
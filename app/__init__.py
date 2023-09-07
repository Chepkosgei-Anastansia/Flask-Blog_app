""" Subdirectory containing  __init__.py is concidered a package and can be imported"""
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler


# Creates application object as an instance of class Flask imported from Flask Package
# __name__ is set to the module in which it is used

app = Flask(__name__)

app.config.from_object(Config) #reads it and applies it
db = SQLAlchemy(app) #db object represents the database
migrate = Migrate(app,db) # object represents migration engine

#crates and initializes the log in extension
login = LoginManager()
login.init_app(app)
#Flask-Login provides a very useful feature that forces users to log in before they can view certain pages of the application. If a user who is not logged in tries to view a protected page, Flask-Login will automatically redirect the user to the login form, and only redirect back to the page the user wanted to view after the login process is complete.
#For this feature to be implemented, Flask-Login needs to know what is the view function that handles logins.
login.login_view = 'login'

from app import routes,models,errors 
import os

# workaround to circular imports

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SEVER'],
                toaddrs=app.config['ADMINS'],subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log',maxBytes=10240,
                       backupCount=10)
        file_handler.setFormatter(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog Application')



            

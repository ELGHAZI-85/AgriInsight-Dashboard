''' 
Set up Flask app with SQLAlchemy database
'''

import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

# Create an instance of SQLAlchemy database
db = SQLAlchemy()

# Manage user login functionality
login_manager = LoginManager()


# Register the app with SQLAlchemy and login manager
def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


# Register Flask blueprints from different modules -> routes & views
def register_blueprints(app):
    for module_name in ('authentication', 'home', 'api'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

# Configure and create the database tables
def configure_database(app):

    @app.before_first_request
    def initialize_database():
        
        try:
            db.create_all()
            
        except Exception as e:
            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

from apps.authentication.oauth import github_blueprint

# Create and configure the app Flask
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)

    app.register_blueprint(github_blueprint, url_prefix="/login") 
    
    configure_database(app)
   
    DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    DB_USERNAME = os.getenv('DB_USERNAME' , None)
    DB_PASS     = os.getenv('DB_PASS'     , None)
    DB_HOST     = os.getenv('DB_HOST'     , None)
    DB_PORT     = os.getenv('DB_PORT'     , None)
    DB_NAME     = os.getenv('DB_NAME'     , None)
        
    return app
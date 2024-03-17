from flask import Flask 
from flask_session import Session
import sqlite3

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "i am so secret"
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['SESSION_PERMANENT'] = False

    Session(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')
    return app

def get_db_connection():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn    

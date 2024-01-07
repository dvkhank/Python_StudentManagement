from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote


app = Flask(__name__)
app.secret_key = '21137affa59a4dd08b708dcf106c724f9'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:%s@localhost/studentmanagement?charset=utf8mb4" % quote('GOT123456')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 2

db = SQLAlchemy(app=app)
login = LoginManager(app=app)



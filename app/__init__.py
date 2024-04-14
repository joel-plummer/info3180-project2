from flask import Flask
from flask_login import LoginManager
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)

from app import views
from app import models
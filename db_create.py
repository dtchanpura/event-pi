from config import SQLALCHEMY_DATABASE_URI
from flask.ext.sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)
